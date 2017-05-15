from __future__ import unicode_literals
from django.db import models
from .mbase import mbase
from .muser import muser
from ..config import clog

# *****************************************************************************
class mcomment(mbase, models.Model):
    user            = models.ForeignKey(muser, on_delete=models.CASCADE,)
    name            = models.CharField(max_length=12)
    thread          = models.CharField(max_length=12)
    subreddit       = models.CharField(max_length=12)
    deleted         = models.BooleanField(default=False)
    def __str__(self):
        # mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        s = self.user.name
        # s += " [" + self.name + "]"
        # s += " [submisson_id=" + self.submission_id + "]"
        # s += " [parent_id=" + self.parent_id + "]"
        return format(s)

# *****************************************************************************
class mcommentRaw(mbase, models.Model):
    index           = models.OneToOneField(mcomment, primary_key=True)   # was uci
    data            = models.TextField()
    def __str__(self):
        # mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        s = self.index.user
        # s += " [" + self.data + "]"
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






