from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from .mbase import mbase
from ..config import clog
import praw
# import pprint

# *****************************************************************************
class mcommentManager(models.Manager):
    def addOrUpdate(self, username, prawComment):
        mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        try:
            i_mcomment = self.get(username=username, name=prawComment.name, thread=prawComment.link_id, subreddit=prawComment.subreddit_id)
            redditFieldDict = i_mcomment.getRedditFieldDict()
            changedCount = i_mcomment.updateRedditFields(prawComment, redditFieldDict)
            if changedCount == 0: i_mcomment.addOrUpdateTempField = "oldUnchanged"
            else:                 i_mcomment.addOrUpdateTempField = "oldChanged"
        except ObjectDoesNotExist:
            # clog.logger.info("username = %s" % (username))
            i_mcomment = self.create(username=username, name=prawComment.name, thread=prawComment.link_id, subreddit=prawComment.subreddit_id)
            redditFieldDict = i_mcomment.getRedditFieldDict()
            i_mcomment.addRedditFields(prawComment, redditFieldDict)
            i_mcomment.addOrUpdateTempField = "new"

        # clog.logger.debug("i_mcomment = %s" % (pprint.pformat(vars(i_mcomment))))
        i_mcomment.save()
        return i_mcomment

# *****************************************************************************
class mcomment(mbase, models.Model):
    name                        = models.CharField(max_length=12)
    thread                      = models.CharField(max_length=12)
    subreddit                   = models.CharField(max_length=12, db_index=True)
    username                    = models.CharField(max_length=30, db_index=True)
    # properties
    pdeleted                    = models.BooleanField(default=False)
    puseradded                  = models.BooleanField(default=False)
    # Reddit fields
    rapproved_by                = models.CharField(max_length=21, default='', blank=True)
    rbanned_by                  = models.CharField(max_length=21, default='', blank=True)
    rid                         = models.CharField(max_length=10, default='', blank=True)
    rparent_id                  = models.CharField(max_length=16, default='', blank=True)
    rsubreddit_name_prefixed    = models.CharField(max_length=64, default='', blank=True)

    rbody                       = models.TextField(default='', blank=True)
    rmod_reports                = models.TextField(default='', blank=True)
    ruser_reports               = models.TextField(default='', blank=True)

    rcontroversiality           = models.IntegerField(default=0)
    rdowns                      = models.IntegerField(default=0)
    rscore                      = models.IntegerField(default=0)
    rups                        = models.IntegerField(default=0)

    rarchived                   = models.BooleanField(default=False)
    rstickied                   = models.BooleanField(default=False)

    rcreated                    = models.DecimalField(default=0, max_digits=12,decimal_places=1)
    rcreated_utc                = models.DecimalField(default=0, max_digits=12,decimal_places=1)
    redited                     = models.DecimalField(default=0, max_digits=12,decimal_places=1)

    objects = mcommentManager()

    # -------------------------------------------------------------------------
    def getRedditFieldDict(self):
        mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        redditFieldDict = {
            # mThreadFieldName          redditFieldName                 convertMethodPtr
            'rapproved_by':             ("approved_by",                 self.getRedditUserNameAsString),  # special
            'rbanned_by':               ("banned_by",                   self.getRedditUserNameAsString),  # special
            'rid':                      ("id",                          None),      # string
            'rparent_id':               ("parent_id",                   None),      # string
            'rsubreddit_name_prefixed': ("subreddit_name_prefixed",     None),      # string

            'rbody':                    ("body",                        None),      # string
            'rmod_reports':             ("mod_reports",                 None),      # [[u'mod reported text', u'stp2007']],  OR [[u'Spam', u'stp2007']]
            'ruser_reports':            ("user_reports",                None),      # [[u'Text for other reason', 1]]        OR [[u'Spam', 1]]

            'rcontroversiality':        ("controversiality",            int),       # int
            'rdowns':                   ("downs",                       int),       # int
            'rscore':                   ("score",                       int),       # int
            'rups':                     ("ups",                         int),       # int

            'rarchived':                ("archived",                    None),      # bool
            'rstickied':                ("stickied",                    None),      # bool

            'rcreated':                 ("created",                     None),      # 1493534605.0,
            'rcreated_utc':             ("created_utc",                 None),      # 1493534605.0,

            'redited':                  ("edited",                      self.getEditedOrFalseValueAsZero),  # False or timestamp

        }
        return redditFieldDict

    # -------------------------------------------------------------------------
    def __str__(self):
        # mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        s = self.username
        # s += " [" + self.name + "]"
        # s += " [submisson_id=" + self.submission_id + "]"
        # s += " [parent_id=" + self.parent_id + "]"
        return format(s)

# # ----------------------------------------------------------------------------
# # COMMENT ATTRIBUTES COMING FROM A USER
# {
#   '_fetched'                      : True,
#   '_info_params'                  : {},
#   '_mod'                          : None,
#   '_reddit'                       : <praw.reddit.Reddit object at 0x7f4e76125eb8>,
#   '_replies'                      : [],
#   '_submission'                   : None,
#   'approved_by'                   : None,
#   'archived'                      : False,
#   'author_flair_css_class'        : None,
#   'author_flair_text'             : None,
#   'author'                        : Redditor(name='stp2007'),
#   'banned_by'                     : None,
#   'body_html'                     : '<div class="md"><p>Thanks</p>\n</div>',
#   'body'                          : 'Thanks\n',
#   'can_gild'                      : True,
#   'controversiality'              : 0,
#   'created_utc'                   : 1492955714.0,
#   'created'                       : 1492984514.0,
#   'distinguished'                 : None,
#   'downs'                         : 0,
#   'edited'                        : False,
#   'gilded'                        : 0,
#   'id'                            : 'dgn3ae1',
#   'likes'                         : None,
#   'link_author'                   : 'stp2007',
#   'link_id'                       : 't3_66ybk6',
#   'link_permalink'                : 'https://www.reddit.com/r/TheWarNerd/comments/66ybk6/radio_war_nerd_questions/',
#   'link_title'                    : 'Radio War Nerd questions',
#   'link_url'                      : 'https://www.reddit.com/r/TheWarNerd/comments/66ybk6/radio_war_nerd_questions/',
#   'mod_reports'                   : [],
#   'name'                          : 't1_dgn3ae1',
#   'num_comments'                  : 4,
#   'num_reports'                   : None,
#   'over_18'                       : False,
#   'parent_id'                     : 't1_dgmugew',
#   'quarantine'                    : False,
#   'removal_reason'                : None,
#   'report_reasons'                : None,
#   'saved'                         : False,
#   'score_hidden'                  : False,
#   'score'                         : 1,
#   'stickied'                      : False,
#   'subreddit_id'                  : 't5_3b93s',
#   'subreddit_name_prefixed'       : 'r/TheWarNerd',
#   'subreddit_type'                : 'public',
#   'subreddit'                     : Subreddit(display_name='TheWarNerd'),
#   'ups'                           : 1,
#   'user_reports'                  : []
# }

# # ----------------------------------------------------------------------------
# # COMMENT ATTRIBUTES COMING FROM A SUBMISSION
# {
#   '_fetched': True,
#   '_info_params': {},
#   '_mod': None,
#   '_reddit': <praw.reddit.Reddit object at 0x7fe085ff5f28>,
#   '_replies': <praw.models.comment_forest.CommentForest object at 0x7fe085433d68>,
#   '_submission': Submission(id='69a8hl'),
#   'approved_by': None,
#   'archived': False,
#   'author_flair_css_class': None,
#   'author_flair_text': None,
#   'author': Redditor(name='AutoModerator'),
#   'banned_by': None,
#   'body_html': '<div class="md"><p>As a reminder, this subreddit <a ',
#   'body': '\nAs a reminder, this subreddit [is for civil ',
#   'can_gild': True,
#   'controversiality': 0,
#   'created_utc': 1493930841.0,
#   'created': 1493959641.0,
#   'depth': 0,
#   'distinguished': 'moderator',
#   'downs': 0,
#   'edited': False,
#   'gilded': 0,
#   'id': 'dh4zdvm',
#   'likes': None,
#   'link_id': 't3_69a8hl',
#   'mod_reports': [],
#   'name': 't1_dh4zdvm',
#   'num_reports': None,
#   'parent_id': 't3_69a8hl',
#   'removal_reason': None,
#   'report_reasons': None,
#   'saved': False,
#   'score_hidden': True,
#   'score': 1,
#   'stickied': True,
#   'subreddit_id': 't5_2cneq',
#   'subreddit_name_prefixed': 'r/politics',
#   'subreddit_type': 'public',
#   'subreddit': Subreddit(display_name='politics'),
#   'ups': 1,
#   'user_reports': []
# }






