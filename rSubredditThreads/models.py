from __future__ import unicode_literals
from django.db import models
from redditCommon.constants import *

# *****************************************************************************
class subreddit(models.Model):
    name        = models.CharField(max_length=30)
    def __str__(self):
        return format(self.name)

# *****************************************************************************
class subredditThreadProcessedStatus(models.Model):
    subreddit   = models.OneToOneField(subreddit, primary_key=True)
    after       = models.CharField(max_length=30, default=CONST_UNPROCESSED)
    before      = models.CharField(max_length=30, default=CONST_UNPROCESSED)
    def __str__(self):
        s = self.subreddit.name
        s += " [After: " + self.after + "]"
        s += " [Before: " + self.before + "]"
        return format(s)

# *****************************************************************************
class subredditThreadIndex(models.Model):
    subreddit   = models.ForeignKey(subreddit, on_delete=models.CASCADE,)
    name        = models.CharField(max_length=12)
    def __str__(self):
        s = self.subreddit.name
        s += " [" + self.name + "]"
        return format(s)

# *****************************************************************************
class subredditThreadRaw(models.Model):
    sti         = models.OneToOneField(subredditThreadIndex, primary_key=True)
    data        = models.TextField()
    title       = models.CharField(max_length=301)      # added so title is easily displayable for testing may remove later
    def __str__(self):
        s = self.sti.subreddit.name
        s += " [" + self.title + "]"
        return format(s)

















