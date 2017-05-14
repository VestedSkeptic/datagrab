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

    # --------------------------------------------------------------------------
    def getBestBeforeValue(self, prawReddit):
        mi = clog.dumpMethodInfo()
        clog.logger.info(mi + " METHOD NOT COMPLETED")
        return ''

    # --------------------------------------------------------------------------
    def updateThreads(self, argDict):
        mi = clog.dumpMethodInfo()
        clog.logger.info(mi)

        prawReddit = self.getPrawRedditInstance()

        params={};
        params['before'] = self.getBestBeforeValue(prawReddit)
        clog.logger.debug("params[before] = %s" % params['before'])


        return