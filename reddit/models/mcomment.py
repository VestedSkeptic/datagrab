from __future__ import unicode_literals
from django.db import models
from .mbase import mbase
from .muser import muser
from .msubreddit import msubreddit
# from .constants import *

# *****************************************************************************
class mcomment(mbase, models.Model):
    user            = models.CharField(max_length=12)
    submission      = models.CharField(max_length=12)
    subreddit       = models.CharField(max_length=12)
    fullName              = models.CharField(max_length=12)
    deleted         = models.BooleanField(default=False)
    def __str__(self):
        s = self.user.name
        # s += " [" + self.name + "]"
        # s += " [submisson_id=" + self.submission_id + "]"
        # s += " [parent_id=" + self.parent_id + "]"
        return format(s)

# *****************************************************************************
class mcommentRaw(mbase, models.Model):
    index          = models.OneToOneField(mcomment, primary_key=True)   # was uci
    data            = models.TextField()
    def __str__(self):
        s = self.index.user
        # s += " [" + self.data + "]"
        return format(s)












