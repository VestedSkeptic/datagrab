from django.core.exceptions import ObjectDoesNotExist
from ..config import clog
from ..models.mcomment import mcomment
from ..models.muser import muser
import praw

# # *****************************************************************************
# # if mcomment exists return it otherwise create it
# def getmcomment(comment, i_muser, aDict):
#     mi = clog.dumpMethodInfo()
#     # clog.logger.info(mi)
#
#     ssi = None
#     try:
#         ssi = mcomment.objects.get(user=i_muser, name=comment.name)
#         aDict['isNew'] = False
#     except ObjectDoesNotExist:
#         ssi = mcomment(user=i_muser, name=comment.name, thread=comment.parent_id, subreddit=comment.subreddit_id)
#         ssi.save()
#     aDict['ssi'] = ssi
#     return

# # *****************************************************************************
# # if mcommentRaw does not exist save it.
# # TODO else compare appropriate fields, if any differences record appropriately
# def savesmcommentRaw(comment, ssi):
#     mi = clog.dumpMethodInfo()
#     # clog.logger.info(mi)
#
#     stRaw = None
#     try:
#         stRaw = mcommentRaw.objects.get(index=ssi)
#         # stRaw = mcomment.mcommentRaw.objects.get(ssi=ssi)
#     except ObjectDoesNotExist:
#         # # vars converts comment to json dict which can be saved to DB
#         # ts = comment
#         # clog.logger.debug("ts.subreddit type = %s " % (type(ts.subreddit)))
#         # clog.logger.debug("ts.author type = %s" % (type(ts.author)))
#         # clog.logger.debug("ts._reddit type = %s" % (type(ts._reddit)))
#
#         stRaw = mcommentRaw(index=ssi, data=vars(comment))
#         # stRaw = mthread.mcommentRaw(ssi=ssi, data=vars(comment))
#         # stRaw = mcommentRaw(ssi=ssi, data=json.dumps(vars(comment)))
#         # stRaw = mcommentRaw(ssi=ssi, data=json.dumps(comment))
#         stRaw.save()
#     return


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
    countDuplicate = 0
    try:
        # for comment in prawReddit.subreddit(i_muser.name).new(limit=None, params=params):
        for comment in prawReddit.redditor(i_muser.name).comments.new(limit=None, params=params):
            # aDict = {'ssi' : None, 'isNew' : True }
            # getmcomment(comment, i_muser, aDict)
            # if aDict['isNew']:
            #     savesmcommentRaw(comment, aDict['ssi'])
            #     countNew += 1
            # else:
            #     countDuplicate += 1
            pass  # REPACE WITH NEW COMMENT MANAGER
    except praw.exceptions.APIException as e:
        clog.logger.error("PRAW APIException: error_type = %s, message = %s" % (e.error_type, e.message))

    s_temp = i_muser.name + ": " + str(countNew) + " new and " + str(countDuplicate) + " duplicate submissions processed"
    clog.logger.info(s_temp)

    return

# *****************************************************************************
def getCommentsByCommentForest(i_mthread, argDict, sortOrder):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    clog.logger.debug("%s: %s: sortOrder = %s" % (i_mthread.subreddit.name, i_mthread.fullname, sortOrder))

    # create PRAW prawReddit instance
    prawReddit = i_mthread.getPrawRedditInstance()

    countNew = 0
    countDuplicate = 0
    countPostsWithNoAuthor = 0
    try:
        params={};

        submissionObject = prawReddit.submission(id=i_mthread.fullname[3:])
        clog.logger.debug("submissionObject = %s" % (submissionObject))

        submissionObject.comment_sort = sortOrder
        # submissionObject.comments.replace_more(limit=0)
        # submissionObject.comments.replace_more(limit=None)
        submissionObject.comments.replace_more(limit=16)
        for comment in submissionObject.comments.list():
            clog.logger.debug("comment = %s" % (comment))
            # See if comment.author.name exists in class user(models.Model):
            # If not add it with ppoi value set to false.
            if comment.author == None:
                countPostsWithNoAuthor += 1
            else:
                # i_muser = None
                # try:
                #     i_muser = muser.objects.get(name=comment.author.name)
                #     clog.logger.debug("muser %s exists" % (i_muser.name))
                # except ObjectDoesNotExist:
                #     i_muser = muser(name=comment.author.name, ppoi=False)
                #     i_muser.save()
                #     clog.logger.trace("muser %s created" % (i_muser.name))
                # replace with iuser manager
                # replace with iuser manager
                # replace with iuser manager
                # replace with iuser manager

                # aDict = {'ssi' : None, 'isNew' : True }
                # # blUserComments_getUserCommentIndex(comment, i_muser, aDict)
                # getmcomment(comment, i_muser, aDict)
                # clog.logger.trace("muser %s needs to be created" % (i_muser.name))
                # if aDict['isNew']:
                #     # blUserComments_saveUserCommentsRaw(comment, aDict['ssi'])
                #     savesmcommentRaw(comment, aDict['ssi'])
                #     countNew += 1
                # else:
                #     countDuplicate += 1
                pass  # REPACE WITH NEW COMMENT MANAGER
    except praw.exceptions.APIException as e:
        clog.logger.error("PRAW APIException: error_type = %s, message = %s" % (e.error_type, e.message))

    # Update i_mthread appropriately
    saveSubIndex = False
    if sortOrder == "new":
        i_mthread.pforestgot = True
        clog.logger.trace("%s: %s: pforestgot set to True" % (i_mthread.subreddit.name, i_mthread.fullname))
        saveSubIndex = True
    if countNew > 0:
        i_mthread.pcount += countNew
        clog.logger.trace("%s: %s: pcount set to %d" % (i_mthread.subreddit.name, i_mthread.fullname, i_mthread.pcount))
        saveSubIndex = True
    if saveSubIndex:
        i_mthread.save()

    s_temp = i_mthread.subreddit.name + ", " + i_mthread.fullname + ": " + str(countNew) + " new, " + str(countDuplicate) + " duplicated, " + str(countPostsWithNoAuthor) + " with no author."
    clog.logger.info(s_temp)
    argDict['rv'] += "<br>" + s_temp
    return

# --------------------------------------------------------------------------
def updateThreadComments(i_mthread, argDict):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = ''
    if not i_mthread.pforestgot:
        clog.logger.trace("%s: %s: New commentForest updating sorted by new" % (i_mthread.subreddit.name, i_mthread.fullname))
        getCommentsByCommentForest(i_mthread, argDict, "new")
        argDict['modeCount']['Comment Forest New'] += 1
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
        argDict['modeCount']['Method To Be Implemented Later'] += 1

    return







