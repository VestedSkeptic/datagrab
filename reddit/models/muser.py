from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from .mbase import mbase
# from .mcomment import mcomment
from ..config import clog
import praw
# import pprint

# *****************************************************************************
class muserManager(models.Manager):
    def addOrUpdate(self, prawRedditor):

        # NOTE: ENDED UP WITH MULITIPLE USERS WITH SAME NAME BECAUSE TWO TASKS operating
        # AT THE SAME TIME CREATED BOTH USERS. THIS CAUSES THE GET CALL BELOW TO FAIL.
        # FOR NOW, BEFORE FIXING THAT ISSUE AND WRITING CODE TO FIX DUPLICATE NAMES AM
        # CHANGING QUERY TO FILTER AND HACKING IN DUPLICATE OF OJBECT DOE SNOT EXIST CODE

        mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        try:
            # clog.logger.info("prawRedditor.name = %s" % (prawRedditor.name))

            # i_muser = self.get(name=prawRedditor.name)
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

        # clog.logger.debug("i_muser = %s" % (pprint.pformat(vars(i_muser))))
        i_muser.save()
        return i_muser

# *****************************************************************************
class muser(mbase, models.Model):
    name            = models.CharField(max_length=30)
    # properties
    ppoi            = models.BooleanField(default=False)
    phistorygot     = models.BooleanField(default=False)
    # Redditor fields
    r_path          = models.CharField(max_length=40, default='', blank=True)

    objects = muserManager()

    # -------------------------------------------------------------------------
    def getRedditFieldDict(self):
        mi = clog.dumpMethodInfo()
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
        if self.phistorygot: s += " (phistorygot = True)"
        else:                s += " (phistorygot = False)"
        return format(s)

    # --------------------------------------------------------------------------
    def getBestCommentBeforeValue(self, prawReddit):
        mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        clog.logger.info("METHOD NOT COMPLETED")
        return ''

    # --------------------------------------------------------------------------
    def updateComments(self):
        from .mcomment import mcomment

        mi = clog.dumpMethodInfo()
        clog.logger.info(mi)

        vs = ''
        prawReddit = self.getPrawRedditInstance()

        params={};
        params['before'] = self.getBestCommentBeforeValue(prawReddit)
        clog.logger.debug("params[before] = %s" % params['before'])

        # iterate through submissions saving them
        countNew = 0
        countOldChanged = 0
        countOldUnchanged = 0
        try:
            for prawComment in prawReddit.redditor(self.name).comments.new(limit=None, params=params):
                i_mcomment = mcomment.objects.addOrUpdate(self, prawComment)
                # clog.logger.debug("i_mcomment = %s" % (pprint.pformat(vars(i_mcomment))))
                if i_mcomment.addOrUpdateTempField == "new":            countNew += 1
                if i_mcomment.addOrUpdateTempField == "oldUnchanged":   countOldUnchanged += 1
                if i_mcomment.addOrUpdateTempField == "oldChanged":     countOldChanged += 1

        except praw.exceptions.APIException as e:
            clog.logger.error("PRAW APIException: error_type = %s, message = %s" % (e.error_type, e.message))

        s_temp = self.name + ": " + str(countNew) + " new, " + str(countOldUnchanged) + " oldUnChanged, " + str(countOldChanged) + " oldChanged "
        clog.logger.info(s_temp)

        return


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







