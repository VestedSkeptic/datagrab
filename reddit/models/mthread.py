from __future__ import unicode_literals
from django.db import models
from mbase import mbase
from msubreddit import msubreddit
from ..config import clog

# *****************************************************************************
# subredditSubmissionIndex
class mthread(mbase, models.Model):
    subreddit       = models.ForeignKey(msubreddit, on_delete=models.CASCADE,)
    name            = models.CharField(max_length=12)
    deleted         = models.BooleanField(default=False)
    cForestGot      = models.BooleanField(default=False)
    count           = models.PositiveIntegerField(default=0)

    def __str__(self):
        # mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        s = self.subreddit.name
        s += " [" + self.name + "]"
        s += " [" + str(self.count) + "]"
        if self.cForestGot: s += " (cForestGot = True)"
        else:               s += " (cForestGot = False)"
        return format(s)

# *****************************************************************************
# class subredditSubmissionRaw(models.Model):
class mthreadRaw(models.Model):
    index           = models.OneToOneField(mthread, primary_key=True)
    data            = models.TextField()

    def __str__(self):
        # mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        s = self.index.subreddit.name
        s += ": " + self.data
        return format(s)

# *****************************************************************************
# class subredditSubmissionFieldsExtracted(models.Model):
class mthreadExtracted(models.Model):
    index           = models.OneToOneField(mthread, primary_key=True)
    author          = models.CharField(max_length=21)
    created_utc     = models.DateTimeField()
    is_self         = models.BooleanField()
    title           = models.CharField(max_length=301)
    selftext        = models.TextField()

    def __str__(self):
        # mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        s = self.index.subreddit.name
        s += ": " + self.title
        return format(s)


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


