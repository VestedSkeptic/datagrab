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







