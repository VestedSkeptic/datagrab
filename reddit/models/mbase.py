from __future__ import unicode_literals
from django.db import models
from ..config import clog
import praw
import inspect
# import pprint

CONST_CLIENT_ID                     = "kcksu9E4VgC0TQ"
CONST_SECRET                        = "Megl7I6XKHtGIQ0T4_q62KiaRQw"
CONST_GRANT_TYPE                    = "client_credentials"
CONST_DEV_USERNAME                  = "OldDevLearningLinux"
CONST_DEV_PASSWORD                  = "899823wef"
CONST_USER_AGENT                    = "test app by /u/OldDevLearningLinux, ver 0.01"

# *****************************************************************************
class mbase(models.Model):
    pass
    def __str__(self):
        return format("mbase")

    # # -------------------------------------------------------------------------
    # @staticmethod
    # def getDictOfClassFieldNames(classModel):
    #     mi = clog.dumpMethodInfo()
    #     clog.logger.info(mi)
    #
    #     rvDict = {}
    #     fields = classModel._meta.get_fields()
    #     for field in fields:
    #         rvDict[field.name] = None
    #     return rvDict

    # -------------------------------------------------------------------------
    @staticmethod
    def getPrawRedditInstance():
        mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        prawReddit = praw.Reddit(
            client_id=CONST_CLIENT_ID,
            client_secret=CONST_SECRET,
            user_agent=CONST_USER_AGENT,
            username=CONST_DEV_USERNAME,
            password=CONST_DEV_PASSWORD
        )
        return prawReddit

    # -------------------------------------------------------------------------
    def getRedditUserNameAsString(self, redditUser):
        mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        if isinstance(redditUser, praw.models.Redditor): return redditUser.name         # if it is a praw Reddit object
        elif redditUser == None:                         return '[None]'
        else:                                            return redditUser              # will also return values of '[deleted]' or ''[removed]'

    # -------------------------------------------------------------------------
    # if None will return ''
    def getStringOrNoneAsEmptyString(self, inputString):
        mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        if inputString == None: return ''
        else:                   return inputString

    # -------------------------------------------------------------------------
    # Reddit edited field has a value of False or a timestamp.
    # This method will return timestamp or a value of zero if it was False
    def getEditedOrFalseValueAsZero(self, inputString):
        mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        if inputString == False:    return 0
        else:                       return inputString

    # -------------------------------------------------------------------------
    def addRedditFields(self, prawData, redditFieldDict):
        mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        for mFieldName in redditFieldDict:
            redditFieldName     = redditFieldDict[mFieldName][0]  # ex: author
            convertMethodPtr    = redditFieldDict[mFieldName][1]  # ex: self.getRedditUserNameAsString
            redditValue         = getattr(prawData, redditFieldName)  # ex: prawData.author

            if convertMethodPtr: setattr(self, mFieldName, convertMethodPtr(redditValue))
            else:                setattr(self, mFieldName, redditValue)

    # -------------------------------------------------------------------------
    # return count of fields that were changed or zero
    def updateRedditFields(self, prawData, redditFieldDict):
        mi = clog.dumpMethodInfo()
        # clog.logger.info(mi)

        # clog.logger.debug("METHOD NOT COMPLETED")

        for mFieldName in redditFieldDict:
            redditFieldName     = redditFieldDict[mFieldName][0]  # ex: author
            convertMethodPtr    = redditFieldDict[mFieldName][1]  # ex: self.getRedditUserNameAsString
            redditValue         = getattr(prawData, redditFieldName)  # ex: prawData.author

            # Instead of only putting value in self
            # - get current value in self
            # - see if different then new value
            # - if different archive/backup current value
            # - then replace current value with new value

            # if convertMethodPtr: setattr(self, mFieldName, convertMethodPtr(redditValue))
            # else:                setattr(self, mFieldName, redditValue)


        return 0




