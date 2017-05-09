from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import subreddit, subredditSubmissionIndex, subredditSubmissionRaw
from mLogging import getmLoggerInstance
from .constants import *
import json
import praw
# import pprint

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
def blSubredditSubmissions_getMostValidBeforeValue(subreddit, reddit):
    logger = getmLoggerInstance()
    youngestRV = ''

    for item in subredditSubmissionIndex.objects.filter(subreddit=subreddit, deleted=False).order_by('-name'):
        # CAN I BATCH THIS QUERY UP TO GET MULTIPLE COMMENTS FROM REDDIT AT ONCE?
        submission = reddit.submission(item.name[3:])
        if submission.author != None:
            youngestRV = item.name
            break
        else: # Update item as deleted.
            item.deleted = True
            item.save()
            logger.debug("subredditSubmissionIndex %s flagged as deleted" % (item.name))


    return youngestRV

# *****************************************************************************
def blSubredditSubmissions_updateThreadsForSubreddits(subreddit, argDict):
    logger = getmLoggerInstance()
    logger.info("Processing subreddit: %s" % (subreddit.name))

    # create PRAW reddit instance
    reddit = praw.Reddit(client_id=CONST_CLIENT_ID, client_secret=CONST_SECRET, user_agent=CONST_USER_AGENT, username=CONST_DEV_USERNAME, password=CONST_DEV_PASSWORD)

    # get youngest subredditSubmissionIndex in DB if there are any
    params={};
    params['before'] = blSubredditSubmissions_getMostValidBeforeValue(subreddit, reddit)
    logger.debug("params[before] = %s" % params['before'])

    # iterate through submissions saving them
    countNew = 0
    countDuplicate = 0
    for submission in reddit.subreddit(subreddit.name).new(limit=None, params=params):
        aDict = {'ssi' : None, 'isNew' : True }
        blSubredditSubmissions_getsubredditSubmissionIndex(submission, subreddit, aDict)
        if aDict['isNew']:
            blSubredditSubmissions_savesubredditSubmissionRaw(submission, aDict['ssi'])
            countNew += 1
        else:
            countDuplicate += 1

    argDict['rv'] += "<br><b>" + subreddit.name + "</b>: " + str(countNew) + " new and " + str(countDuplicate) + " duplicate submissions processed"
    return

# *****************************************************************************
def blSubredditSubmissions_updateForAllSubreddits():
    logger = getmLoggerInstance()
    logger.info("=====================================================")
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






































