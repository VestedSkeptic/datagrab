from __future__ import unicode_literals
from django.db import models
from .constants import *

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

# *****************************************************************************
class subreddit(models.Model):
    name        = models.CharField(max_length=30)
    def __str__(self):
        return format(self.name)

# *****************************************************************************
class subredditSubmissionIndex(models.Model):
    subreddit   = models.ForeignKey(subreddit, on_delete=models.CASCADE,)
    name        = models.CharField(max_length=12)
    iidd        = models.CharField(max_length=9)
    def __str__(self):
        s = self.subreddit.name
        s += " [" + self.name + "]" + " [" + self.iidd + "]"
        return format(s)

# *****************************************************************************
class subredditSubmissionRaw(models.Model):
    sti         = models.OneToOneField(subredditSubmissionIndex, primary_key=True)
    data        = models.TextField()
    title       = models.CharField(max_length=301)      # added so title is easily displayable for testing may remove later
    def __str__(self):
        s = self.sti.subreddit.name
        s += " [" + self.title + "]"
        return format(s)














