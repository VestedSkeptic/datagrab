from django.core.exceptions import ObjectDoesNotExist
from ..config import clog
from ..models.mcomment import mcomment, mcommentRaw
import praw

# *****************************************************************************
# if mcomment exists return it otherwise create it
def getmcomment(comment, i_muser, aDict):
    ssi = None
    try:
        ssi = mcomment.objects.get(user=i_muser, name=comment.name)
        aDict['isNew'] = False
    except ObjectDoesNotExist:
        ssi = mcomment(user=i_muser, name=comment.name, thread=comment.parent_id, subreddit=comment.subreddit_id)
        ssi.save()
    aDict['ssi'] = ssi
    return

# *****************************************************************************
# if mcommentRaw does not exist save it.
# TODO else compare appropriate fields, if any differences record appropriately
def savesmcommentRaw(comment, ssi):
    stRaw = None
    try:
        stRaw = mcommentRaw.objects.get(index=ssi)
        # stRaw = mcomment.mcommentRaw.objects.get(ssi=ssi)
    except ObjectDoesNotExist:
        # # vars converts comment to json dict which can be saved to DB
        # ts = comment
        # clog.logger.debug("ts.subreddit type = %s " % (type(ts.subreddit)))
        # clog.logger.debug("ts.author type = %s" % (type(ts.author)))
        # clog.logger.debug("ts._reddit type = %s" % (type(ts._reddit)))

        stRaw = mcommentRaw(index=ssi, data=vars(comment))
        # stRaw = mthread.mcommentRaw(ssi=ssi, data=vars(comment))
        # stRaw = mcommentRaw(ssi=ssi, data=json.dumps(vars(comment)))
        # stRaw = mcommentRaw(ssi=ssi, data=json.dumps(comment))
        stRaw.save()
    return


# --------------------------------------------------------------------------
def getBestBeforeValue(i_muser, prawReddit):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi + " METHOD NOT COMPLETED")
    return ''

# --------------------------------------------------------------------------
def updateUserComments(i_muser):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)
    vs = mi

    prawReddit = i_muser.getPrawRedditInstance()
    # prawReddit = getPrawRedditInstance()

    print("prawReddit = %s" % (prawReddit))

    params={};
    params['before'] = getBestBeforeValue(i_muser, prawReddit)
    clog.logger.debug("params[before] = %s" % params['before'])

    # iterate through submissions saving them
    countNew = 0
    countDuplicate = 0
    try:
        # for comment in prawReddit.subreddit(i_muser.name).new(limit=None, params=params):
        for comment in prawReddit.redditor(i_muser.name).comments.new(limit=None, params=params):
            aDict = {'ssi' : None, 'isNew' : True }
            getmcomment(comment, i_muser, aDict)
            if aDict['isNew']:
                savesmcommentRaw(comment, aDict['ssi'])
                countNew += 1
            else:
                countDuplicate += 1
    except praw.exceptions.APIException as e:
        clog.logger.error("PRAW APIException: error_type = %s, message = %s" % (e.error_type, e.message))

    s_temp = i_muser.name + ": " + str(countNew) + " new and " + str(countDuplicate) + " duplicate submissions processed"
    clog.logger.info(s_temp)

    return
