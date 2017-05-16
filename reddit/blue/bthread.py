# from django.core.exceptions import ObjectDoesNotExist
from ..config import clog
from ..models.mthread import mthread, mthreadManager
import praw
# import pprint

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

    countNew = 0
    countOldUnchanged = 0
    countOldChanged = 0
    try:
        for prawThread in prawReddit.subreddit(i_msubreddit.name).new(limit=None, params=params):
            i_mthread = mthread.objects.addOrUpdate(i_msubreddit, prawThread)
            # clog.logger.debug("i_mthread = %s" % (pprint.pformat(vars(i_mthread))))

            if i_mthread.addOrUpdateTempField == "new":             countNew += 1
            if i_mthread.addOrUpdateTempField == "oldUnchanged":    countOldUnchanged += 1
            if i_mthread.addOrUpdateTempField == "oldChanged":      countOldChanged += 1

    except praw.exceptions.APIException as e:
        clog.logger.error("PRAW APIException: error_type = %s, message = %s" % (e.error_type, e.message))

    clog.logger.info(i_msubreddit.name + ": " + str(countNew) + " new, " + str(countOldUnchanged) + " oldUnchanged, " + str(countOldChanged) + " oldChanged, ")

    return
