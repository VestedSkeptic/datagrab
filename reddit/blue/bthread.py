# from django.core.exceptions import ObjectDoesNotExist
from ..config import clog
from ..models.mthread import mthread, mthreadManager
import praw

# --------------------------------------------------------------------------
def getBestBeforeValue(prawReddit):
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)

    clog.logger.info("METHOD NOT COMPLETED")
    return ''

# --------------------------------------------------------------------------
def getMoreThreadsForSubreddit(i_msubreddit):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = ''
    prawReddit = i_msubreddit.getPrawRedditInstance()

    params={};
    params['before'] = getBestBeforeValue(prawReddit)
    clog.logger.debug("params[before] = %s" % params['before'])

    try:
        for prawThread in prawReddit.subreddit(i_msubreddit.name).new(limit=None, params=params):
            i_mthread = mthread.objects.addOrUpdate(i_msubreddit, prawThread)


    except praw.exceptions.APIException as e:
        clog.logger.error("PRAW APIException: error_type = %s, message = %s" % (e.error_type, e.message))

    # s_temp = i_msubreddit.name + ": " + str(countNew) + " new and " + str(countDuplicate) + " duplicate submissions processed"
    # clog.logger.info(s_temp)

    return
