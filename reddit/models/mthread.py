from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from .mbase import mbase
from .msubreddit import msubreddit
from ..config import clog
import praw
# import pprint

# *****************************************************************************
class mthreadManager(models.Manager):
    def addOrUpdate(self, i_msubreddit, prawThread):
        # mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        try:
            i_mthread = self.get(subreddit=i_msubreddit, fullname=prawThread.name)
            redditFieldDict = i_mthread.getRedditFieldDict()
            changedCount = i_mthread.updateRedditFields(prawThread, redditFieldDict)
            if changedCount == 0: i_mthread.addOrUpdateTempField = "oldUnchanged"
            else:                 i_mthread.addOrUpdateTempField = "oldChanged"
        except ObjectDoesNotExist:
            i_mthread = self.create(subreddit=i_msubreddit, fullname=prawThread.name)
            redditFieldDict = i_mthread.getRedditFieldDict()
            i_mthread.addRedditFields(prawThread, redditFieldDict)
            i_mthread.addOrUpdateTempField = "new"

        # clog.logger.debug("i_mthread = %s" % (pprint.pformat(vars(i_mthread))))
        i_mthread.save()
        return i_mthread

# *****************************************************************************
class mthread(mbase, models.Model):
    subreddit       = models.ForeignKey(msubreddit, on_delete=models.CASCADE,)
    fullname        = models.CharField(max_length=12)
    # properties
    pdeleted        = models.BooleanField(default=False)
    pforestgot      = models.BooleanField(default=False)
    pcount          = models.PositiveIntegerField(default=0)
    # Redditor fields
    rapproved_by    = models.CharField(max_length=21, default='', blank=True)
    rauthor         = models.CharField(max_length=21, default='', blank=True)
    rbanned_by      = models.CharField(max_length=21, default='', blank=True)
    rdomain         = models.CharField(max_length=64, default='', blank=True)
    rid             = models.CharField(max_length=10, default='', blank=True)
    rtitle          = models.CharField(max_length=301, default='', blank=True)
    rurl            = models.CharField(max_length=2084, default='', blank=True)

    rmod_reports    = models.TextField(default='', blank=True)
    rselftext       = models.TextField(default='')
    ruser_reports   = models.TextField(default='', blank=True)

    rdowns          = models.IntegerField(default=0)
    rnum_comments   = models.IntegerField(default=0)
    rscore          = models.IntegerField(default=0)
    rups            = models.IntegerField(default=0)

    rhidden         = models.BooleanField(default=False)
    ris_self        = models.BooleanField(default=False)
    rlocked         = models.BooleanField(default=False)
    rquarantine     = models.BooleanField(default=False)

    rcreated        = models.DecimalField(default=0, max_digits=12,decimal_places=1)
    rcreated_utc    = models.DecimalField(default=0, max_digits=12,decimal_places=1)
    redited         = models.DecimalField(default=0, max_digits=12,decimal_places=1)

    objects = mthreadManager()

    # -------------------------------------------------------------------------
    def getRedditFieldDict(self):
        # mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        redditFieldDict = {
            # mThreadFieldName      redditFieldName     convertMethodPtr
            'rapproved_by':         ("approved_by",     self.getRedditUserNameAsString),  # special
            'rauthor':              ("author",          self.getRedditUserNameAsString),  # special
            'rbanned_by':           ("banned_by",       self.getRedditUserNameAsString),  # special
            'rdomain':              ("domain",          None),      # string
            'rid':                  ("id",              None),      # string
            'rtitle':               ("title",           None),      # string
            'rurl':                 ("url",             None),      # string

            'rmod_reports':         ("mod_reports",     None),      # [[u'mod reported text', u'stp2007']],  OR [[u'Spam', u'stp2007']]
            'rselftext':            ("selftext",        None),      # string
            'ruser_reports':        ("user_reports",    None),      # [[u'Text for other reason', 1]]        OR [[u'Spam', 1]]

            'rdowns':               ("downs",           int),       # int
            'rnum_comments':        ("num_comments",    int),       # int
            'rscore':               ("score",           int),       # int
            'rups':                 ("ups",             int),       # int

            'rhidden':              ("hidden",          None),      # bool
            'ris_self':             ("is_self",         None),      # bool
            'rlocked':              ("locked",          None),      # bool
            'rquarantine':          ("quarantine",      None),      # bool

            'rcreated':             ("created",         None),      # 1493534605.0,
            'rcreated_utc':         ("created_utc",     None),      # 1493534605.0,

            'redited':              ("edited",          self.getEditedOrFalseValueAsZero),  # False or timestamp
        }
        return redditFieldDict

    # -------------------------------------------------------------------------
    def __str__(self):
        # mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        s = self.subreddit.name
        s += " [" + self.fullname + "]"
        s += " [" + str(self.pcount) + "]"
        if self.pforestgot: s += " (pforestgot = True)"
        else:               s += " (pforestgot = False)"
        return format(s)

    # *****************************************************************************
    # def getCommentsByCommentForest(self, argDict, sortOrder):
    def getCommentsByCommentForest(self, sortOrder):
        from .mcomment import mcomment
        from .muser import muser

        mi = clog.dumpMethodInfo()
        # clog.logger.debug(mi)
        # clog.logger.debug("%s: %s: sortOrder = %s" % (self.subreddit.name, self.fullname, sortOrder))

        # create PRAW prawReddit instance
        prawReddit = self.getPrawRedditInstance()

        countNew = 0
        countOldChanged = 0
        countOldUnchanged = 0
        countPostsWithNoAuthor = 0
        try:
            params={};

            submissionObject = prawReddit.submission(id=self.fullname[3:])
            submissionObject.comment_sort = sortOrder
            # submissionObject.comments.replace_more(limit=0)
            # submissionObject.comments.replace_more(limit=None)
            submissionObject.comments.replace_more(limit=16)
            for prawComment in submissionObject.comments.list():
                if prawComment.author == None:
                    countPostsWithNoAuthor += 1
                else:
                    # prawRedditor = prawReddit.redditor(prawComment.author.name)
                    # i_muser = muser.objects.addOrUpdate(prawRedditor)
                    # # clog.logger.debug("i_muser = %s" % (pprint.pformat(vars(i_muser))))

                    i_mcomment = mcomment.objects.addOrUpdate(prawComment.author.name, prawComment)
                    # clog.logger.debug("i_mcomment = %s" % (pprint.pformat(vars(i_mcomment))))
                    if i_mcomment.addOrUpdateTempField == "new":            countNew += 1
                    if i_mcomment.addOrUpdateTempField == "oldUnchanged":   countOldUnchanged += 1
                    if i_mcomment.addOrUpdateTempField == "oldChanged":     countOldChanged += 1

        except praw.exceptions.APIException as e:
            clog.logger.error("PRAW APIException: error_type = %s, message = %s" % (e.error_type, e.message))

        # Update self appropriately
        save_mthread = False
        if sortOrder == "new":
            self.pforestgot = True
            save_mthread = True
        if countNew > 0:
            self.pcount += countNew
            save_mthread = True
        if save_mthread:
            self.save()

        s_temp = str(countNew) + " new, " + str(countOldUnchanged) + " oldUnchanged, " + str(countOldChanged) + " oldChanged, " + str(countPostsWithNoAuthor) + " with no author."
        clog.logger.info(s_temp)
        return

    # --------------------------------------------------------------------------
    def updateComments(self):
        mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        vs = ''
        if not self.pforestgot:
            clog.logger.trace("%s: %s: New commentForest updating sorted by new" % (self.subreddit.name, self.fullname))
            # getCommentsByCommentForest(self, argDict, "new")
            self.getCommentsByCommentForest("new")
            # argDict['modeCount']['Comment Forest New'] += 1
        # elif self.count < 10:
        #     clog.logger.debug("%s: %s: Old small commentForest updating sorted by old" % (self.subreddit.name, self.fullname))
        #     getCommentsByCommentForest(self, argDict, "old")
            # argDict['modeCount']['Comment Forest Old'] += 1
                        # THIS HACK NOT VALID, SUBMISSION UPDATED AND HAS NEW COUNT NOW
                        # elif self.count == 260:  #HACK THERE IS ONE ITEM WITH 260 COUNT IN IT, USING IT TO TEST IMPLEMENTATION OF ...
                        #     clog.logger.debug("%s: %s: Old small commentForest updating sorted by old" % (self.subreddit.name, self.fullname))
                        #     getCommentsByCommentForest(self, argDict, "old")
                        #     argDict['modeCount']['Comment Forest Old'] += 1
        else:
            clog.logger.info("%s: %s: Old large commentForest updating by METHOD TO BE IMPLEMENTED LATER" % (self.subreddit.name, self.fullname))
        return


# # ----------------------------------------------------------------------------
# # SUBMISSION attributes
# # EX:
# # subreddit = reddit.subreddit('redditdev')
# # submission = subreddit.hot(limit=1).next()
# # logger.info(submission.title)  # to make it non-lazy
# # pprint.pprint(vars(submission))
# {
#   '_comments_by_id': {},
#   '_fetched': False,
#   '_flair': None,
#   '_info_params': {},
#   '_mod': None,
#   '_reddit': <praw.reddit.Reddit object at 0x7fee4ac8beb8>,
#   'approved_by': None,
#   'archived': False,
#   'author_flair_css_class': None,
#   'author_flair_text': None,
#   'author': Redditor(name='bboe'),
#   'banned_by': None,
#   'brand_safe': True,
#   'can_gild': True,
#   'clicked': False,
#   'comment_limit': 2048,
#   'comment_sort': 'best',
#   'contest_mode': False,
#   'created_utc': 1493534605.0,
#   'created': 1493563405.0,
#   'distinguished': None,
#   'domain': 'self.redditdev',
#   'downs': 0,
#   'edited': False,
#   'gilded': 0,
#   'hidden': False,
#   'hide_score': False,
#   'id': '68e6pp',
#   'is_self': True,
#   'likes': None,
#   'link_flair_css_class': None,
#   'link_flair_text': None,
#   'locked': False,
#   'media_embed': {},
#   'media': None,
#   'mod_reports': [],
#   'name': 't3_68e6pp',
#   'num_comments': 0,
#   'num_reports': None,
#   'over_18': False,
#   'permalink': '/r/redditdev/comments/68e6pp/praw_450_released/',
#   'quarantine': False,
#   'removal_reason': None,     # This attribute is deprecated. Please use mod_reports and user_reports instead.
#   'report_reasons': None,     # This attribute is deprecated. Please use mod_reports and user_reports instead.
#   'saved': False,
#   'score': 18,
#   'secure_media_embed': {},
#   'secure_media': None,
#   'selftext_html': '<!-- SC_OFF --><div class="md"><p>Notable additions:</p>\n',
#   'selftext': 'Notable additions:\n',
#   'spoiler': False,
#   'stickied': True,
#   'subreddit_id': 't5_2qizd',
#   'subreddit_name_prefixed': 'r/redditdev',
#   'subreddit_type': 'public',
#   'subreddit': Subreddit(display_name='redditdev'),
#   'suggested_sort': None,
#   'thumbnail': '',
#   'title': 'PRAW 4.5.0 Released',
#   'ups': 18,
#   'url': 'https://www.reddit.com/r/redditdev/comments/68e6pp/praw_450_released/',
#   'user_reports': [],
#   'view_count': None,
#   'visited': False
# }


