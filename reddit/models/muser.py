from __future__ import unicode_literals
from django.db import models
from .mbase import mbase

# *****************************************************************************
class muser(mbase, models.Model):
    name            = models.CharField(max_length=30)
    poi             = models.BooleanField(default=False)
    cHistoryGot     = models.BooleanField(default=False)
    def __str__(self):
        s = self.name
        if self.poi: s += " (poi)"
        if self.cHistoryGot: s += " (cHistoryGot = True)"
        else:                s += " (cHistoryGot = False)"
        return format(s)











