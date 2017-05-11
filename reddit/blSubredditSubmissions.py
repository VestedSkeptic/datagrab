from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import subreddit, subredditSubmissionIndex, subredditSubmissionRaw, subredditSubmissionFieldsExtracted, getDictOfClassModelFieldNames, getFieldValueFromRawData
from mLogging import getmLoggerInstance
from .constants import *
import json
import praw
import pprint

# *****************************************************************************
# if subredditSubmissionIndex exists return it otherwise create it
def blSubredditSubmissions_getsubredditSubmissionIndex(submission, subreddit, aDict):
    ssi = None
    try:
        ssi = subredditSubmissionIndex.objects.get(subreddit=subreddit, name=submission.name)
        aDict['isNew'] = False
    except ObjectDoesNotExist:
        ssi = subredditSubmissionIndex(subreddit=subreddit, name=submission.name)
        ssi.save()
    aDict['ssi'] = ssi
    return

# *****************************************************************************
# if subredditSubmissionRaw does not exist save it.
# TODO else compare appropriate fields, if any differences record appropriately
def blSubredditSubmissions_savesubredditSubmissionRaw(submission, ssi):
    # logger = getmLoggerInstance()
    stRaw = None
    try:
        stRaw = subredditSubmissionRaw.objects.get(ssi=ssi)
    except ObjectDoesNotExist:
        # # vars converts submission to json dict which can be saved to DB
        # ts = submission
        # logger.debug("ts.subreddit type = %s " % (type(ts.subreddit)))
        # logger.debug("ts.author type = %s" % (type(ts.author)))
        # logger.debug("ts._reddit type = %s" % (type(ts._reddit)))

        stRaw = subredditSubmissionRaw(ssi=ssi, data=vars(submission))
        # stRaw = subredditSubmissionRaw(ssi=ssi, data=json.dumps(vars(submission)))
        # stRaw = subredditSubmissionRaw(ssi=ssi, data=json.dumps(submission))
        stRaw.save()
    return

# *****************************************************************************
def blSubredditSubmissions_getMostValidBeforeValue(subreddit, prawReddit):
    logger = getmLoggerInstance()
    youngestRV = ''

    for item in subredditSubmissionIndex.objects.filter(subreddit=subreddit, deleted=False).order_by('-name'):
        try:
            # CAN I BATCH THIS QUERY UP TO GET MULTIPLE COMMENTS FROM REDDIT AT ONCE?
            submission = prawReddit.submission(item.name[3:])
            if submission.author != None:
                youngestRV = item.name
                # when before value is failing as it was in politics
                # HERE examine what is in submission as I likely need a better
                # test then if submission.author != NoneAdapter
                # pprint.pprint(vars(submission))
                logger.trace(pprint.pformat(vars(submission)))
                break
            else: # Update item as deleted.
                item.deleted = True
                item.save()
                logger.debug("subredditSubmissionIndex %s flagged as deleted" % (item.name))
        except praw.exceptions.APIException(error_type, message, field):
            logger.error("PRAW APIException: error_type = %s, message = %s" % (error_type, message))

    return youngestRV

# *****************************************************************************
def blSubredditSubmissions_updateThreadsForSubreddits(subreddit, argDict):
    logger = getmLoggerInstance()
    # logger.info("Processing subreddit: %s" % (subreddit.name))

    # create prawReddit instance
    prawReddit = praw.Reddit(client_id=CONST_CLIENT_ID, client_secret=CONST_SECRET, user_agent=CONST_USER_AGENT, username=CONST_DEV_USERNAME, password=CONST_DEV_PASSWORD)

    # get youngest subredditSubmissionIndex in DB if there are any
    params={};
    params['before'] = blSubredditSubmissions_getMostValidBeforeValue(subreddit, prawReddit)
    logger.debug("params[before] = %s" % params['before'])

    # iterate through submissions saving them
    countNew = 0
    countDuplicate = 0
    try:
        for submission in prawReddit.subreddit(subreddit.name).new(limit=None, params=params):
            aDict = {'ssi' : None, 'isNew' : True }
            blSubredditSubmissions_getsubredditSubmissionIndex(submission, subreddit, aDict)
            if aDict['isNew']:
                blSubredditSubmissions_savesubredditSubmissionRaw(submission, aDict['ssi'])
                countNew += 1
                logger.debug("Added submission: %s" % (submission.title[:40]))
            else:
                countDuplicate += 1
    except praw.exceptions.APIException as e:
        logger.error("PRAW APIException: error_type = %s, message = %s" % (e.error_type, e.message))

    s_temp = subreddit.name + ": " + str(countNew) + " new and " + str(countDuplicate) + " duplicate submissions processed"
    logger.info(s_temp)
    argDict['rv'] += "<br>" + s_temp
    return

# *****************************************************************************
def blSubredditSubmissions_updateForAllSubreddits():
    logger = getmLoggerInstance()
    logger.info("=====================================================")
    logger.info("blSubredditSubmissions_updateForAllSubreddits")
    rv = "<B>PRAW</B> blSubredditSubmissions_updateForAllSubreddits<BR>"

    subreddits = subreddit.objects.all()
    if subreddits.count() == 0:
        rv += "<BR> No subreddits found"
    else:
        for su in subreddits:
            argDict = {'rv': ""}
            blSubredditSubmissions_updateThreadsForSubreddits(su, argDict)
            rv += argDict['rv']
    logger.info("=====================================================")
    return HttpResponse(rv)

# *****************************************************************************
def blSubredditSubmissions_deleteAllSubreddits():
    logger = getmLoggerInstance()
    s = "blSubredditSubmissions_deleteAllSubreddits(): "
    qs = subreddit.objects.all()
    sqsCount = qs.count()
    # delete all subreddit objects
    qs.delete()
    s += str(sqsCount) + " subreddits deleted"
    logger.info(s)
    return s

# *****************************************************************************
def blSubredditSubmissions_addSubreddit(sname):
    logger = getmLoggerInstance()
    s = "blSubredditSubmissions_addSubreddit(" + sname + "): "
    try:
        subreddit.objects.get(name=sname)
        s += "already exists"
    except ObjectDoesNotExist:
        sr = subreddit(name=sname)
        sr.save()
        s += "added"
    logger.info(s)
    return s

# *****************************************************************************
def blSubredditSubmissions_deleteAll_SSFE():
    logger = getmLoggerInstance()
    s = "blSubredditSubmissions_deleteAll_SSFE(): "
    qs = subredditSubmissionFieldsExtracted.objects.all()
    sqsCount = qs.count()
    # delete all subredditSubmissionFieldsExtracted objects
    qs.delete()
    s += str(sqsCount) + " deleted"
    logger.info(s)
    return s

# *****************************************************************************
def blSubredditSubmissions_updateAll_SSFE():
    logger = getmLoggerInstance()
    s = "blSubredditSubmissions_updateAll_SSFE(): "

    qs = subredditSubmissionRaw.objects.all()

    rawCount = qs.count()
    countExists = 0
    countNew = 0
    for rawSubmissonItem in qs:
        try:
            subredditSubmissionFieldsExtracted.objects.get(ssi=rawSubmissonItem.ssi)
            countExists += 1
        except ObjectDoesNotExist:
            fnDict = getDictOfClassModelFieldNames(subredditSubmissionFieldsExtracted)
            # if ssi is in fnDict remove it
            if 'ssi' in fnDict: del fnDict['ssi']
            # logger.info(pprint.pformat(fnDict))

            # get values for each field from
            for k in fnDict:
                # logger.info(k)
                fnDict[k] = getFieldValueFromRawData(k, rawSubmissonItem.data)
                logger.info("BLUEBLUEBLUE: %s" % (rawSubmissonItem.data))

                if fnDict[k] == None:
                    # data retreival failed
                    pass



            # sr = subreddit(**fnDict)
            # sr.save()
            countNew += 1



    s += "rawCount = " + str(rawCount)
    s += ", countExists = " + str(countExists)
    s += ", countNew = " + str(countNew)

    logger.info(s)
    return s































