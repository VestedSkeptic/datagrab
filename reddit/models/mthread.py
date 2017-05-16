from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from mbase import mbase
from msubreddit import msubreddit
from ..config import clog

# *****************************************************************************
class mthreadManager(models.Manager):
    def addOrUpdate(self, i_msubreddit, prawThread):
        mi = clog.dumpMethodInfo()
        clog.logger.info(mi)

        try:
            i_mthread = self.get(subreddit=i_msubreddit, name=prawThread.name)
            # i_mthread.updateRedditFields(prawThread)
        except ObjectDoesNotExist:
            i_mthread = self.create(subreddit=i_msubreddit, name=prawThread.name)
            redditFieldDict = i_mthread.getRedditFieldDict()
            i_mthread.addRedditFields(prawThread, redditFieldDict)
        i_mthread.save()


        # Return results such as
        # new item
        # old item, unchanged
        # old item, changed

        return i_mthread

# *****************************************************************************
class mthread(mbase, models.Model):
    subreddit       = models.ForeignKey(msubreddit, on_delete=models.CASCADE,)
    name            = models.CharField(max_length=12)
    # rename following as properties, ex: pdeleted, pforestgot, pcount
    pdeleted        = models.BooleanField(default=False)
    pforestgot      = models.BooleanField(default=False)
    pcount          = models.PositiveIntegerField(default=0)
    # rename following as reddit fields: ex" redited, rdomain, etc.
    rauthor          = models.CharField(max_length=21, default='', blank=True)
    rdowns           = models.IntegerField(default=0)
    rups             = models.IntegerField(default=0)
    rtitle           = models.CharField(max_length=301, default='', blank=True)
    rselftext        = models.TextField(default='')
    ris_self         = models.BooleanField(default=False)

    objects = mthreadManager()

    # -------------------------------------------------------------------------
    def __str__(self):
        # mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        s = self.subreddit.name
        s += " [" + self.name + "]"
        s += " [" + str(self.pcount) + "]"
        if self.pforestgot: s += " (pforestgot = True)"
        else:               s += " (pforestgot = False)"
        return format(s)

    # -------------------------------------------------------------------------
    def getRedditFieldDict(self):
        mi = clog.dumpMethodInfo()
        clog.logger.info(mi)

        redditFieldDict = {
            # mThreadFieldName      redditFieldName     convertMethodPtr
            'rauthor':              ("author",          self.getRedditAuthorName),
            'rdowns':               ("downs",           int),
            'rups':                 ("ups",             int),
            'rtitle':               ("title",           None),
            'rselftext':            ("selftext",        None),
            'ris_self':             ("is_self",         None),

        }
        return redditFieldDict

    # -------------------------------------------------------------------------
    def getRedditAuthorName(self, author):
        mi = clog.dumpMethodInfo()
        clog.logger.info(mi)

        if author == None or author == '[deleted]' or author == '[removed]': return author
        else:                                                                return author.name



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
#   'removal_reason': None,
#   'report_reasons': None,
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


