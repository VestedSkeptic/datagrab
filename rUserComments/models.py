from __future__ import unicode_literals
from django.db import models
from redditCommon.constants import *

# *****************************************************************************
class user(models.Model):
    name        = models.CharField(max_length=30)
    def __str__(self):
        return format(self.name)

# *****************************************************************************
class userCommentsProcessedStatus(models.Model):
    user        = models.OneToOneField(user, primary_key=True)
    after       = models.CharField(max_length=30, default=CONST_UNPROCESSED)
    before      = models.CharField(max_length=30, default=CONST_UNPROCESSED)
    def __str__(self):
        s = self.user.name
        s += " [After: " + self.after + "]"
        s += " [Before: " + self.before + "]"
        return format(s)

# *****************************************************************************
class userCommentsIndex(models.Model):
    user        = models.ForeignKey(user, on_delete=models.CASCADE,)
    name        = models.CharField(max_length=12)
    def __str__(self):
        s = self.user.name
        s += " [" + self.name + "]"
        return format(s)

# *****************************************************************************
class userCommentsRaw(models.Model):
    uci         = models.OneToOneField(userCommentsIndex, primary_key=True)
    data        = models.TextField()
    def __str__(self):
        s = self.uci.user.name
        s += " [" + self.data + "]"
        return format(s)




# GET [/r/subreddit]/comments/article
# apu call uses the threads ID not its name
# ID:       "68ot5m",
# name":    "t3_68ot5m",




# Probably want to add a field to user
# POI with default value of false
# Only if poi is true do I grab all of their comments.
# Will allow adding users to same DB table as I parse comment threads without automatically grabbing all of this users comments_updateForAllUsers():


# THESE FIELDS RETURNED WHEN DIRECTLY QUERYING A USERS comments
# COMPARE THIS TO THE FIELDS RETURNED FOR COMMENTS FROM A THREAD
            # "approved_by": null,
            # "archived": false,
            # "author_flair_css_class": null,
            # "author_flair_text": null,
            # "author": "OldDevLearningLinux",
            # "banned_by": null,
            # "body_html": "&lt;div class=\"md\"&gt;&lt;p&gt;Reply 30a&lt;/p&gt;\n&lt;/div&gt;",
            # "body": "Reply 30a",
            # "can_gild": true,
            # "controversiality": 0
            # "created_utc": 1493579948.0,
            # "created": 1493608748.0,
            # "distinguished": null,
            # "downs": 0,
            # "edited": false,
            # "gilded": 0,
            # "id": "dgyf703",
            # "likes": null,
            # "link_author": "OldDevLearningLinux",           # this field not in the other listing
            # "link_id": "t3_5xnbad",
            # # THESE NEXT THREE FIELDS NO FOUND IN OTHER LISTING
            # "link_permalink": "https://www.reddit.com/r/test/comments/5xnbad/test_thread_01/",
            # "link_title":
            # "link_url": "https://www.reddit.com/r/test/comments/5xnbad/test_thread_01/",
            # "mod_reports": [],
            # "name": "t1_dgyf703",
            # "num_comments": 36,                             # this field not in the other listing
            # "num_reports": null,
            # "over_18": false,                               # this field not in the other listing
            # "parent_id": "t3_5xnbad",
            # "quarantine": false,                            # this field not in the other listing
            # "removal_reason": null,
            # "replies": "",
            # "report_reasons": null,
            # "saved": false,
            # "score_hidden": false,
            # "score": 1,
            # "stickied": false,
            # "subreddit_id": "t5_2qh23",
            # "subreddit_name_prefixed": "r/test",
            # "subreddit_type": "public",
            # "subreddit": "test",
            # "Test Thread 01",                                # this field not in the other listing
            # "ups": 1,
            # "user_reports": [],







