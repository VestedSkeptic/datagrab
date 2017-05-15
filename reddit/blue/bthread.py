from django.core.exceptions import ObjectDoesNotExist
from ..config import clog
from ..models.mthread import mthread, mthreadRaw
import praw

# *****************************************************************************
# if mthread exists return it otherwise create it
def getmthread(prawThread, i_msubreddit, aDict):
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)

    ssi = None
    try:
        ssi = mthread.objects.get(subreddit=i_msubreddit, name=prawThread.name)
        aDict['isNew'] = False
    except ObjectDoesNotExist:
        ssi = mthread(subreddit=i_msubreddit, name=prawThread.name)
        ssi.save()
    aDict['ssi'] = ssi
    return

# *****************************************************************************
# if mthreadRaw does not exist save it.
# TODO else compare appropriate fields, if any differences record appropriately
def savesmthreadRaw(submission, ssi):
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)

    stRaw = None
    try:
        stRaw = mthreadRaw.objects.get(index=ssi)
        # stRaw = mthread.mthreadRaw.objects.get(ssi=ssi)
    except ObjectDoesNotExist:
        # # vars converts submission to json dict which can be saved to DB
        # ts = submission
        # clog.logger.debug("ts.subreddit type = %s " % (type(ts.subreddit)))
        # clog.logger.debug("ts.author type = %s" % (type(ts.author)))
        # clog.logger.debug("ts._reddit type = %s" % (type(ts._reddit)))

        stRaw = mthreadRaw(index=ssi, data=vars(submission))
        # stRaw = mthread.mthreadRaw(ssi=ssi, data=vars(submission))
        # stRaw = mthreadRaw(ssi=ssi, data=json.dumps(vars(submission)))
        # stRaw = mthreadRaw(ssi=ssi, data=json.dumps(submission))
        stRaw.save()
    return


# --------------------------------------------------------------------------
def getBestBeforeValue(prawReddit):
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)

    clog.logger.info("METHOD NOT COMPLETED")
    return ''

# --------------------------------------------------------------------------
def updateSubredditThreads(i_msubreddit):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = ''
    prawReddit = i_msubreddit.getPrawRedditInstance()

    params={};
    params['before'] = getBestBeforeValue(prawReddit)
    clog.logger.debug("params[before] = %s" % params['before'])

    # iterate through submissions saving them
    countNew = 0
    countDuplicate = 0
    try:
        for prawThread in prawReddit.subreddit(i_msubreddit.name).new(limit=None, params=params):
            aDict = {'ssi' : None, 'isNew' : True }
            getmthread(prawThread, i_msubreddit, aDict)
            if aDict['isNew']:
                savesmthreadRaw(prawThread, aDict['ssi'])
                countNew += 1
                clog.logger.debug("Added prawThread: %s" % (prawThread.title[:40]))
            else:
                countDuplicate += 1
    except praw.exceptions.APIException as e:
        clog.logger.error("PRAW APIException: error_type = %s, message = %s" % (e.error_type, e.message))

    s_temp = i_msubreddit.name + ": " + str(countNew) + " new and " + str(countDuplicate) + " duplicate submissions processed"
    clog.logger.info(s_temp)

    return
