from __future__ import unicode_literals
from django.db import models
from .defines import *

# *****************************************************************************
class user(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return format(self.name)

# *****************************************************************************
class userCommentProcessedStatus(models.Model):
    # user = models.ForeignKey(user, on_delete=models.CASCADE, primary_key=True)
    # user = models.ForeignKey(user, on_delete=models.CASCADE, unique=True)
    user = models.OneToOneField(user, primary_key=True)

    # after = models.CharField(max_length=30, default=CONST_UNPROCESSED, blank=True, null=True)
    after  = models.CharField(max_length=30, default=CONST_UNPROCESSED)
    before = models.CharField(max_length=30, default=CONST_UNPROCESSED)
    def __str__(self):
        s = self.user.name
        s += " [After: " + self.after + "]"
        s += " [Before: " + self.before + "]"
        return format(s)