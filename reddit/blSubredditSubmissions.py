from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import subreddit, subredditSubmissionIndex, subredditSubmissionRaw
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
    stRaw = None
    try:
        stRaw = subredditSubmissionRaw.objects.get(ssi=ssi)
    except ObjectDoesNotExist:
        # vars converts submission to json dict which can be saved to DB
        stRaw = subredditSubmissionRaw(ssi=ssi, data=vars(submission))
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






































