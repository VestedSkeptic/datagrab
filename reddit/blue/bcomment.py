from django.core.exceptions import ObjectDoesNotExist
from ..config import clog
from ..models.mcomment import mcomment
from ..models.muser import muser
import praw
# import pprint

# --------------------------------------------------------------------------
def getBestBeforeValue(i_muser, prawReddit):
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)

    clog.logger.info("METHOD NOT COMPLETED")
    return ''

# --------------------------------------------------------------------------
def updateUserComments(i_muser):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = ''
    prawReddit = i_muser.getPrawRedditInstance()

    params={};
    params['before'] = getBestBeforeValue(i_muser, prawReddit)
    clog.logger.debug("params[before] = %s" % params['before'])

    # iterate through submissions saving them
    countNew = 0
    countOldChanged = 0
    countOldUnchanged = 0
    try:
        for prawComment in prawReddit.redditor(i_muser.name).comments.new(limit=None, params=params):
            i_mcomment = mcomment.objects.addOrUpdate(i_muser, prawComment)
            clog.logger.debug("i_mcomment = %s" % (pprint.pformat(vars(i_mcomment))))

            if i_mcomment.addOrUpdateTempField == "new":            countNew += 1
            if i_mcomment.addOrUpdateTempField == "oldUnchanged":   countOldUnchanged += 1
            if i_mcomment.addOrUpdateTempField == "oldChanged":     countOldChanged += 1

    except praw.exceptions.APIException as e:
        clog.logger.error("PRAW APIException: error_type = %s, message = %s" % (e.error_type, e.message))

    s_temp = i_muser.name + ": " + str(countNew) + " new, " + str(countOldUnchanged) + " oldUnChanged, " + str(countOldChanged) + " oldChanged "
    clog.logger.info(s_temp)

    return

# *****************************************************************************
# def getCommentsByCommentForest(i_mthread, argDict, sortOrder):
def getCommentsByCommentForest(i_mthread, sortOrder):
    mi = clog.dumpMethodInfo()
    # clog.logger.debug(mi)
    # clog.logger.debug("%s: %s: sortOrder = %s" % (i_mthread.subreddit.name, i_mthread.fullname, sortOrder))

    # create PRAW prawReddit instance
    prawReddit = i_mthread.getPrawRedditInstance()

    countNew = 0
    countOldChanged = 0
    countOldUnchanged = 0
    countPostsWithNoAuthor = 0
    try:
        params={};

        submissionObject = prawReddit.submission(id=i_mthread.fullname[3:])
        submissionObject.comment_sort = sortOrder
        # submissionObject.comments.replace_more(limit=0)
        # submissionObject.comments.replace_more(limit=None)
        submissionObject.comments.replace_more(limit=16)
        for prawComment in submissionObject.comments.list():
            if prawComment.author == None:
                countPostsWithNoAuthor += 1
            else:
                prawRedditor = prawReddit.redditor(prawComment.author.name)
                i_muser = muser.objects.addOrUpdate(prawRedditor)
                # clog.logger.debug("i_muser = %s" % (pprint.pformat(vars(i_muser))))

                i_mcomment = mcomment.objects.addOrUpdate(i_muser, prawComment)
                # clog.logger.debug("i_mcomment = %s" % (pprint.pformat(vars(i_mcomment))))

                if i_mcomment.addOrUpdateTempField == "new":            countNew += 1
                if i_mcomment.addOrUpdateTempField == "oldUnchanged":   countOldUnchanged += 1
                if i_mcomment.addOrUpdateTempField == "oldChanged":     countOldChanged += 1

    except praw.exceptions.APIException as e:
        clog.logger.error("PRAW APIException: error_type = %s, message = %s" % (e.error_type, e.message))

    # Update i_mthread appropriately
    save_mthread = False
    if sortOrder == "new":
        i_mthread.pforestgot = True
        save_mthread = True
    if countNew > 0:
        i_mthread.pcount += countNew
        save_mthread = True
    if save_mthread:
        i_mthread.save()

    s_temp = i_mthread.subreddit.name + ", " + i_mthread.fullname + ": " + str(countNew) + " new, " + str(countOldUnchanged) + " oldUnchanged, " + str(countOldChanged) + " oldChanged, " + str(countPostsWithNoAuthor) + " with no author."
    clog.logger.info(s_temp)
    # argDict['rv'] += "<br>" + s_temp
    return

# --------------------------------------------------------------------------
# def updateThreadComments(i_mthread, argDict):
def updateThreadComments(i_mthread):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = ''
    if not i_mthread.pforestgot:
        clog.logger.trace("%s: %s: New commentForest updating sorted by new" % (i_mthread.subreddit.name, i_mthread.fullname))
        # getCommentsByCommentForest(i_mthread, argDict, "new")
        getCommentsByCommentForest(i_mthread, "new")
        # argDict['modeCount']['Comment Forest New'] += 1
    # elif i_mthread.count < 10:
    #     clog.logger.debug("%s: %s: Old small commentForest updating sorted by old" % (i_mthread.subreddit.name, i_mthread.fullname))
    #     getCommentsByCommentForest(i_mthread, argDict, "old")
        # argDict['modeCount']['Comment Forest Old'] += 1
                    # THIS HACK NOT VALID, SUBMISSION UPDATED AND HAS NEW COUNT NOW
                    # elif i_mthread.count == 260:  #HACK THERE IS ONE ITEM WITH 260 COUNT IN IT, USING IT TO TEST IMPLEMENTATION OF ...
                    #     clog.logger.debug("%s: %s: Old small commentForest updating sorted by old" % (i_mthread.subreddit.name, i_mthread.fullname))
                    #     getCommentsByCommentForest(i_mthread, argDict, "old")
                    #     argDict['modeCount']['Comment Forest Old'] += 1
    else:
        clog.logger.info("%s: %s: Old large commentForest updating by METHOD TO BE IMPLEMENTED LATER" % (i_mthread.subreddit.name, i_mthread.fullname))
        # argDict['modeCount']['Method To Be Implemented Later'] += 1

    return







