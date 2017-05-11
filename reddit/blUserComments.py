from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import user, userCommentsIndex, userCommentsRaw
from mLogging import getmLoggerInstance
from .constants import *
import json
import praw
import pprint

# *****************************************************************************
# if userCommentsIndex exists return it otherwise create it
def blUserComments_getUserCommentIndex(comment, user, aDict):
    uci = None
    try:
        uci = userCommentsIndex.objects.get(user=user, name=comment.name)
        aDict['isNew'] = False
    except ObjectDoesNotExist:
        uci = userCommentsIndex(user=user, name=comment.name, parent_id=comment.parent_id, submission_id=comment.link_id)
        uci.save()
    aDict['uci'] = uci
    return

# *****************************************************************************
# if blUserComments_saveUserCommentsRaw does not exist save it.
# TODO else compare appropriate fields, if any differences record appropriately
def blUserComments_saveUserCommentsRaw(comment, uci):
    ucr = None
    try:
        ucr = userCommentsRaw.objects.get(uci=uci)
    except ObjectDoesNotExist:
        # vars converts comment to json dict which can be saved to DB
        ucr = userCommentsRaw(uci=uci, data=vars(comment))
        ucr.save()
    return

# *****************************************************************************
def blUserComments_getMostValidBeforeValue(user, prawReddit, forceGetAllHistory=False):
    logger = getmLoggerInstance()
    youngestRV = ''

    if not user.cHistoryGot:
        forceGetAllHistory = True
        user.cHistoryGot = True
        user.save()
        logger.debug("user %s cHistoryGot set to True" % (user.name))

    if not forceGetAllHistory:
        qs = userCommentsIndex.objects.filter(user=user, deleted=False).order_by('-name')
        for item in qs:
            try:
                # CAN I BATCH THIS QUERY UP TO GET MULTIPLE COMMENTS FROM REDDIT AT ONCE?
                comment = prawReddit.comment(item.name[3:])
                # if comment.author != None and comment.author.name.lower() == user.name.lower():
                if comment.author != None:
                    youngestRV = item.name
                    break
                else: # Update item as deleted.
                    item.deleted = True
                    item.save()
                    logger.debug("userCommentIndex %s flagged as deleted" % (item.name))
            except praw.exceptions.APIException as e:
                logger.error("PRAW APIException: error_type = %s, message = %s" % (e.error_type, e.message))
    else:
        logger.debug("cHistoryGot set to True")

    return youngestRV

# *****************************************************************************
def blUserComments_updateCommentsForUser(user, argDict):
    logger = getmLoggerInstance()
    logger.info("Processing user: %s" % (user.name))

    # create prawReddit instance
    prawReddit = praw.Reddit(client_id=CONST_CLIENT_ID, client_secret=CONST_SECRET, user_agent=CONST_USER_AGENT, username=CONST_DEV_USERNAME, password=CONST_DEV_PASSWORD)

    # get youngest userCommentsIndex in DB if there are any
    params={};
    params['before'] = blUserComments_getMostValidBeforeValue(user, prawReddit)
    logger.debug("params[before] = %s" % params['before'])

    # iterate through comments saving them
    countNew = 0
    countDuplicate = 0
    try:
        for comment in prawReddit.redditor(user.name).comments.new(limit=None, params=params):
            aDict = {'uci' : None, 'isNew' : True }
            blUserComments_getUserCommentIndex(comment, user, aDict)
            if aDict['isNew']:
                blUserComments_saveUserCommentsRaw(comment, aDict['uci'])
                countNew += 1
            else:
                countDuplicate += 1
    except praw.exceptions.APIException as e:
        logger.error("PRAW APIException: error_type = %s, message = %s" % (e.error_type, e.message))

    s_temp = user.name + ": " + str(countNew) + " new and " + str(countDuplicate) + " duplicate comments processed"
    logger.info(s_temp)
    argDict['rv'] += "<br>" + s_temp
    return

# *****************************************************************************
def blUserComments_updateForAllUsers():
    logger = getmLoggerInstance()
    logger.info("=====================================================")
    logger.info("blUserComments_updateForAllUsers")
    rv = "<B>PRAW</B> blUserComments_updateForAllUsers<BR>"

    users = user.objects.filter(poi=True)
    if users.count() == 0:
        rv += "<BR> No users found"
    else:
        for us in users:
            argDict = {'rv': ""}
            blUserComments_updateCommentsForUser(us, argDict)
            rv += argDict['rv']
    logger.info("=====================================================")
    return HttpResponse(rv)

# *****************************************************************************
def getDictOfCommentsAtLevel(submissionName, hLevel):
    logger = getmLoggerInstance()
    logger.info("submissioName = %s" %(submissionName))
    logger.info("hLevel = %d" %(hLevel))

    levelCount = 0
    listOfParents = [submissionName]
    resultsDict = {}

    while levelCount <= hLevel:
        logger.info("listOfParents = %s" % (pprint.pformat(listOfParents)))

        # Get all userCommentsIndex which have a parent_id in listOfParents
        qs = userCommentsIndex.objects.filter(submission_id=submissionName).filter(parent_id__in=listOfParents).order_by('name')
        # qs = userCommentsIndex.objects.filter(parent_id__in=listOfParents).order_by('name')
        logger.info("qs.count() = %d" % (qs.count()))

        # clear listOfParents
        del listOfParents[:]

        for item in qs:
            if (levelCount == hLevel):
                resultsDict[item.name] = 0;
            else:
                listOfParents.append(item.name)


            # logger.info("%s: (parent_id = %s) is in list %s " %(item.name, item.parent_id, pprint.pformat(listOfParents)))

        levelCount += 1


    logger.info("----------------------------------------------------")
    logger.info("levelCount = %d" % (levelCount))
    logger.info("hLevel = %d" % (hLevel))
    logger.info("listOfParents = %s" % (pprint.pformat(listOfParents)))
    logger.info("resultsDict = %s" % (pprint.pformat(resultsDict)))





    return {}

# *****************************************************************************
def getHierarchyOfCommentsAtLevel(submissionName, hLevel):
    logger = getmLoggerInstance()
    logger.info("=====================================================")
    logger.info("getHierarchyOfCommentsAtLevel")
    rv = "<B>PRAW</B> getHierarchyOfCommentsAtLevel<BR>"

    dictOfResults = getDictOfCommentsAtLevel(submissionName, hLevel)
    logger.debug(pprint.pformat(dictOfResults))

    logger.info("=====================================================")

    return HttpResponse(rv)











