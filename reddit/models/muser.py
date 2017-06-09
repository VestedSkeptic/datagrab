from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from .mbase import mbase
from ..config import clog
from datetime import datetime
from django.utils import timezone
import praw
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
# class muser(mbase, models.Model):
class muser(mbase):
    name                        = models.CharField(max_length=30, db_index=True)
    # properties
    ppoi                        = models.BooleanField(default=False)
    # precentlyupdated            = models.BooleanField(default=False)
    pprioritylevel              = models.IntegerField(default=0)
    # pcommentsupdatetimestamp    = models.DateTimeField(default=datetime(2000, 1, 1, 1, 0, 0))
    # pcommentsupdatetimestamp    = models.DateTimeField(default=timezone.now())
    # pcommentsupdatetimestamp    = models.DateTimeField(default=timezone.now)
    pcommentsupdatetimestamp    = models.DateTimeField(default=timezone.make_aware(datetime(2000, 1, 1, 1, 0, 0)))
    pupdateswithnochanges       = models.IntegerField(default=0)
    pcountnew                   = models.IntegerField(default=0)
    pcountOldUnchanged          = models.IntegerField(default=0)
    pcountOldChanged            = models.IntegerField(default=0)
    pdeleted                    = models.BooleanField(default=False)
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
        from .mcomment import mcomment
        # mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        youngestRV = ''
        qs = mcomment.objects.filter(username=self.name, pdeleted=False).order_by('-name')
        for item in qs:
            try:
                # CAN I BATCH THIS QUERY UP TO GET MULTIPLE COMMENTS FROM REDDIT AT ONCE?
                isValidComment = prawReddit.comment(item.name[3:])
                # if isValidComment.author != None:
                # if isValidComment.author != None and isValidComment.author.name != '[deleted]' and isValidComment.author.name != '[removed]':
                if isValidComment.author != None and isValidComment.author != '[deleted]' and isValidComment.author != '[removed]':
                    youngestRV = item.name
                    # clog.logger.debug("youngestRV = %s" % (youngestRV))
                    break
                else: # Update item as deleted.
                    item.pdeleted = True
                    item.save()
                    # clog.logger.debug("userCommentIndex %s flagged as deleted" % (item.name))
            except praw.exceptions.APIException as e:
                clog.logger.error("PRAW APIException: error_type = %s, message = %s" % (e.error_type, e.message))

        return youngestRV

    # --------------------------------------------------------------------------
    def commentsUpdated(self, countNew, countOldUnchanged, countOldChanged):
        mi = clog.dumpMethodInfo()
        # self.precentlyupdated =True

        if countNew > 0:
            self.pprioritylevel -= 1
            self.pupdateswithnochanges = 0
            if self.pprioritylevel < 0:
                self.pprioritylevel = 0;
        else:
            self.pprioritylevel += 1
            self.pupdateswithnochanges += 1
            if self.pprioritylevel > 3:
                self.pprioritylevel = 3;

        self.pcountnew          = countNew
        self.pcountOldUnchanged = countOldUnchanged
        self.pcountOldChanged   = countOldChanged

        # self.pcommentsupdatetimestamp = datetime.now()
        self.pcommentsupdatetimestamp = timezone.now()
        self.save()
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







