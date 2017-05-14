from __future__ import unicode_literals
from django.db import models
from .mbase import mbase
# from .mthread import mthread
# from .. import config
from ..config import clog

# *****************************************************************************
class msubreddit(mbase, models.Model):
    name            = models.CharField(max_length=30)
    poi             = models.BooleanField(default=False)
    def __str__(self):
        s = self.name
        if self.poi: s += " (poi)"
        return format(s)

