from __future__ import unicode_literals
from django.db import models
from redditCommon.constants import *

# *****************************************************************************
class user(models.Model):
    name        = models.CharField(max_length=30)
    poi         = models.BooleanField(default=False)
    def __str__(self):
        s = self.name
        if self.poi:
            s += " (poi)"
        return format(s)

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










