from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from .mbase import mbase
from ..config import clog
import pprint

# *****************************************************************************
class msubredditManager(models.Manager):
    def addOrUpdate(self, name, prawSubreddit):
        mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        try:
            i_msubreddit = self.get(name=name)
            redditFieldDict = i_msubreddit.getRedditFieldDict()
            changedCount = i_msubreddit.updateRedditFields(prawSubreddit, redditFieldDict)
            if changedCount == 0: i_msubreddit.addOrUpdateTempField = "oldUnchanged"
            else:                 i_msubreddit.addOrUpdateTempField = "oldChanged"
        except ObjectDoesNotExist:
            i_msubreddit = self.create(name=name)
            redditFieldDict = i_msubreddit.getRedditFieldDict()
            i_msubreddit.addRedditFields(prawSubreddit, redditFieldDict)
            i_msubreddit.addOrUpdateTempField = "new"

        clog.logger.info("i_msubreddit = %s" % (pprint.pformat(vars(i_msubreddit))))
        i_msubreddit.save()
        return i_msubreddit

# *****************************************************************************
# class msubreddit(mbase, models.Model):
class msubreddit(mbase):
    name                            = models.CharField(max_length=30)
    # properties
    ppoi                            = models.BooleanField(default=False)
    precentlyupdated                = models.BooleanField(default=False)

#   priority level
#   timestamp of update


    # Redditor fields
    raccounts_active_is_fuzzed      = models.BooleanField(default=False)
    rcollapse_deleted_comments      = models.BooleanField(default=False)
    rpublic_traffic                 = models.BooleanField(default=False)
    rquarantine                     = models.BooleanField(default=False)
    rshow_media_preview             = models.BooleanField(default=False)
    rshow_media                     = models.BooleanField(default=False)
    rspoilers_enabled               = models.BooleanField(default=False)
    rhide_ads                       = models.BooleanField(default=False)
    rover18                         = models.BooleanField(default=False)

    raccounts_active                = models.IntegerField(default=0)
    rcomment_score_hide_mins        = models.IntegerField(default=0)
    rsubscribers                    = models.IntegerField(default=0)

    rdescription                    = models.TextField(default='')
    rpublic_description             = models.TextField(default='')

    rdisplay_name                   = models.CharField(max_length=100, default='', blank=True)
    rlang                           = models.CharField(max_length=20, default='', blank=True)
    rid                             = models.CharField(max_length=12, default='', blank=True)
    rsubmission_type                = models.CharField(max_length=12, default='', blank=True)
    rsubreddit_type                 = models.CharField(max_length=12, default='', blank=True)
    rtitle                          = models.CharField(max_length=101, default='', blank=True)
    rurl                            = models.CharField(max_length=40, default='', blank=True)
    rwhitelist_status               = models.CharField(max_length=24, default='', blank=True)

    rcreated_utc                    = models.DecimalField(default=0, max_digits=12,decimal_places=1)
    rcreated                        = models.DecimalField(default=0, max_digits=12,decimal_places=1)

    radvertiser_category            = models.TextField(default='')
    rwiki_enabled                   = models.TextField(default='')

    objects = msubredditManager()

    # -------------------------------------------------------------------------
    def getRedditFieldDict(self):
        mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        redditFieldDict = {
            # mThreadFieldName              redditFieldName                 convertMethodPtr
            'raccounts_active_is_fuzzed':   ("accounts_active_is_fuzzed",   None),      # bool
            'rcollapse_deleted_comments':   ("collapse_deleted_comments",   None),      # bool
            'rpublic_traffic':              ("public_traffic",              None),      # bool
            'rquarantine':                  ("quarantine",                  None),      # bool
            'rshow_media_preview':          ("show_media_preview",          None),      # bool
            'rshow_media':                  ("show_media",                  None),      # bool
            'rspoilers_enabled':            ("spoilers_enabled",            None),      # bool
            'rhide_ads':                    ("hide_ads",                    None),      # bool
            'rover18':                      ("over18",                      None),      # bool

            'raccounts_active':             ("accounts_active",             int),       # int
            'rcomment_score_hide_mins':     ("comment_score_hide_mins",     int),       # int
            'rsubscribers':                 ("subscribers",                 int),       # int

            'rdescription':                 ("description",                 None),      # string text area
            'rpublic_description':          ("public_description",          None),      # string text area

            'rdisplay_name':                ("display_name",                None),      # string
            'rlang':                        ("lang",                        None),      # string
            'rid':                          ("id",                          None),      # string
            'rsubmission_type':             ("submission_type",             None),      # string
            'rsubreddit_type':              ("subreddit_type",              None),      # string
            'rtitle':                       ("title",                       None),      # string
            'rurl':                         ("url",                         None),      # string
            'rwhitelist_status':            ("whitelist_status",            self.getStringOrNoneAsEmptyString),      # string

            'rcreated_utc':                 ("created_utc",                 None),      # 1493534605.0,
            'rcreated':                     ("created",                     None),      # 1493534605.0,

            'radvertiser_category':         ("advertiser_category",         self.getStringOrNoneAsEmptyString),      # string text area
            'rwiki_enabled':                ("wiki_enabled",                self.getStringOrNoneAsEmptyString),      # string text are
        }
        return redditFieldDict

    # -------------------------------------------------------------------------
    def __str__(self):
        # mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        s = self.name
        # if self.ppoi: s += " (ppoi)"
        return format(s)

    # --------------------------------------------------------------------------
    def getThreadsBestBeforeValue(self, prawReddit):
        mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        # clog.logger.info("METHOD NOT COMPLETED")
        return ''

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

