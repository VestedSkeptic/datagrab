from __future__ import unicode_literals
from django.db import models
from .mbase import mbase
from ..config import clog

# *****************************************************************************
class msubreddit(mbase, models.Model):
    name            = models.CharField(max_length=30)
    poi             = models.BooleanField(default=False)
    def __str__(self):
        # mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        s = self.name
        if self.poi: s += " (poi)"
        return format(s)


# # ----------------------------------------------------------------------------
# # SUBREDDIT attributes
# {
#   '_banned': None,
#   '_comments': None,
#   '_contributor': None,
#   '_fetched': True,
#   '_filters': None,
#   '_flair': None,
#   '_info_params': {},
#   '_mod': None,
#   '_moderator': None,
#   '_modmail': None,
#   '_muted': None,
#   '_path': 'r/redditdev/',
#   '_quarantine': None,
#   '_reddit': <praw.reddit.Reddit object at 0x7f1474006e48>,
#   '_stream': None,
#   '_stylesheet': None,
#   '_wiki': None,
#   'accounts_active_is_fuzzed': True,
#   'accounts_active': 9,
#   'advertiser_category': None,
#   'allow_images': False,
#   'banner_img': '',
#   'banner_size': None,
#   'collapse_deleted_comments': False,
#   'comment_score_hide_mins': 0,
#   'created_utc': 1213802177.0,
#   'created': 1213830977.0,
#   'description_html': '<!-- SC_OFF --><div class="md"><p>A subreddit for '
#   'description': 'A subreddit for discussion of reddit API clients and the ',
#   'display_name_prefixed': 'r/redditdev',
#   'display_name': 'redditdev',
#   'header_img': 'https://e.thumbs.redditmedia.com/bOToSJt13ylszjE4.png',
#   'header_size': [120, 40],
#   'header_title': None,
#   'hide_ads': False,
#   'icon_img': '',
#   'icon_size': None,
#   'id': '2qizd',
#   'key_color': '#ff4500',
#   'lang': 'en',
#   'name': 't5_2qizd',
#   'over18': False,
#   'public_description_html': '<!-- SC_OFF --><div class="md"><p>A subreddit for ',
#   'public_description': 'A subreddit for discussion of reddit API clients and ',
#   'public_traffic': True,
#   'quarantine': False,
#   'show_media_preview': False,
#   'show_media': False,
#   'spoilers_enabled': False,
#   'submission_type': 'self',
#   'submit_link_label': None,
#   'submit_text_html': '<!-- SC_OFF --><div class="md"><p>Get faster, better ',
#   'submit_text_label': None,
#   'submit_text': 'Get faster, better responses by including more information, ',
#   'subreddit_type': 'public',
#   'subscribers': 10887,
#   'suggested_comment_sort': None,
#   'title': 'reddit Development',
#   'url': '/r/redditdev/',
#   'user_is_banned': False,
#   'user_is_contributor': False,
#   'user_is_moderator': False,
#   'user_is_muted': False,
#   'user_is_subscriber': False,
#   'user_sr_theme_enabled': False,
#   'whitelist_status': 'all_ads',
#   'wiki_enabled': None
#  }

