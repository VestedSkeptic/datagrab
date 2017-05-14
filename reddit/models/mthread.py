from __future__ import unicode_literals
from django.db import models
from mbase import mbase
from msubreddit import msubreddit

# *****************************************************************************
# subredditSubmissionIndex
class mthread(mbase, models.Model):
    subreddit       = models.ForeignKey(msubreddit, on_delete=models.CASCADE,)
    name            = models.CharField(max_length=12)
    deleted         = models.BooleanField(default=False)
    cForestGot      = models.BooleanField(default=False)
    count           = models.PositiveIntegerField(default=0)
    def __str__(self):
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
        s = self.index.subreddit.name
        s += ": " + self.title
        return format(s)
