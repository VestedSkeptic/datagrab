from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from .mbase import mbase
from ..config import clog
# import praw
# import pprint

# *****************************************************************************
class muserManager(models.Manager):
    def addOrUpdate(self, prawRedditor):
        # mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        # NOTE: ENDED UP WITH MULITIPLE USERS WITH SAME NAME BECAUSE TWO TASKS operating
        # AT THE SAME TIME CREATED BOTH USERS. THIS CAUSES THE GET CALL BELOW TO FAIL.
        # FOR NOW, BEFORE FIXING THAT ISSUE AND WRITING CODE TO FIX DUPLICATE NAMES AM
        # CHANGING QUERY TO FILTER AND HACKING IN DUPLICATE OF OJBECT DOE SNOT EXIST CODE
        try:
            qs = muser.objects.filter(name=prawRedditor.name)
            if qs.count() > 0:
                i_muser = qs[0]
                redditFieldDict = i_muser.getRedditFieldDict()
                changedCount = i_muser.updateRedditFields(prawRedditor, redditFieldDict)
                if changedCount == 0: i_muser.addOrUpdateTempField = "oldUnchanged"
                else:                 i_muser.addOrUpdateTempField = "oldChanged"
            else: # hack put in object does not exist code below
                i_muser = self.create(name=prawRedditor.name)
                redditFieldDict = i_muser.getRedditFieldDict()
                i_muser.addRedditFields(prawRedditor, redditFieldDict)
                i_muser.addOrUpdateTempField = "new"
        except ObjectDoesNotExist:
            i_muser = self.create(name=prawRedditor.name)
            redditFieldDict = i_muser.getRedditFieldDict()
            i_muser.addRedditFields(prawRedditor, redditFieldDict)
            i_muser.addOrUpdateTempField = "new"

        i_muser.save()
        return i_muser

# *****************************************************************************
class muser(mbase, models.Model):
    name                        = models.CharField(max_length=30, db_index=True)
    # properties
    ppoi                        = models.BooleanField(default=False)
    precentlyupdated            = models.BooleanField(default=False)
    # Redditor fields
    r_path                      = models.CharField(max_length=40, default='', blank=True)

    objects = muserManager()

    # -------------------------------------------------------------------------
    def getRedditFieldDict(self):
        # mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        redditFieldDict = {
            # mThreadFieldName      redditFieldName     convertMethodPtr
            'r_path':               ("_path",           None),      # string
        }
        return redditFieldDict

    # -------------------------------------------------------------------------
    def __str__(self):
        # mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)
        s = self.name
        if self.ppoi: s += " (ppoi)"
        return format(s)

    # --------------------------------------------------------------------------
    def getBestCommentBeforeValue(self, prawReddit):
        # mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        # clog.logger.info("METHOD NOT COMPLETED")
        return ''

# # ----------------------------------------------------------------------------
# # REDDITOR attributes
# # Ex
# # rUser = reddit.redditor('stp2007')
# # logger.info(rUser.name) # to make it non-lazy
# # pprint.pprint(vars(rUser))
# {
#   '_fetched':           False,
#   '_info_params':       {},
#   '_listing_use_sort':  True,
#   '_path':              'user/stp2007/',
#   '_reddit':            <praw.reddit.Reddit object at 0x7f45d99f9128>,
#   'name':               'stp2007'
#  }







