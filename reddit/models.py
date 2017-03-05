from __future__ import unicode_literals
from django.db import models
from .defines import *

# *****************************************************************************
class user(models.Model):
    name    = models.CharField(max_length=30)
    def __str__(self):
        return format(self.name)

# *****************************************************************************
class userCommentsProcessedStatus(models.Model):
    user    = models.OneToOneField(user, primary_key=True)
    after   = models.CharField(max_length=30, default=CONST_UNPROCESSED)
    before  = models.CharField(max_length=30, default=CONST_UNPROCESSED)
    def __str__(self):
        s = self.user.name
        s += " [After: " + self.after + "]"
        s += " [Before: " + self.before + "]"
        return format(s)