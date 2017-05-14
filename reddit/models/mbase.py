from __future__ import unicode_literals
from django.db import models
from .. import config
from ..config import clog
# from config import clog
import praw

CONST_CLIENT_ID                                         = "kcksu9E4VgC0TQ"
CONST_SECRET                                            = "Megl7I6XKHtGIQ0T4_q62KiaRQw"
CONST_GRANT_TYPE                                        = "client_credentials"
CONST_DEV_USERNAME                                      = "OldDevLearningLinux"
CONST_DEV_PASSWORD                                      = "899823wef"
CONST_USER_AGENT                                        = "test app by /u/OldDevLearningLinux, ver 0.01"

# *****************************************************************************
class mbase(models.Model):
    pass
    def __str__(self):
        return format("mbase")

    # -------------------------------------------------------------------------
    @staticmethod
    def getDictOfClassFieldNames(classModel):
        rvDict = {}
        fields = classModel._meta.get_fields()
        for field in fields:
            rvDict[field.name] = None
        return rvDict

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







