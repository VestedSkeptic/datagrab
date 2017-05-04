from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import subreddit, subredditThreadProcessedStatus, subredditThreadIndex, subredditThreadRaw
from .constants import *
import json
import praw
import pprint

# *****************************************************************************
# get subredditThreadProcessedStatus for subreddit, if not exist create on
def getSubredditThreadProcessedStatus(subreddit):
    cs = None
    try:
        cs = subredditThreadProcessedStatus.objects.get(subreddit=subreddit)
    except ObjectDoesNotExist:
        cs = subredditThreadProcessedStatus(subreddit=subreddit)
        cs.save()
    return cs

# *****************************************************************************
# if subredditThreadIndex exists return it otherwise create it
def getSubredditThreadIndex(thread, subreddit, aDict):
    sti = None
    try:
        sti = subredditThreadIndex.objects.get(subreddit=subreddit, name=thread.name)
        aDict['isNew'] = False
    except ObjectDoesNotExist:
        sti = subredditThreadIndex(subreddit=subreddit, name=thread.name)
        sti.save()
    aDict['sti'] = sti
    return

# *****************************************************************************
# if subredditThreadRaw does not exist save it.
# TODO else compare appropriate fields, if any differences record appropriately
def saveSubredditThreadRaw(thread, sti):
    stRaw = None
    try:
        stRaw = subredditThreadRaw.objects.get(sti=sti)
    except ObjectDoesNotExist:
        # vars converts thread to json dict which can be saved to DB
        stRaw = subredditThreadRaw(sti=sti, data=vars(thread), title=thread.title)
        stRaw.save()
    return

# *****************************************************************************
def updateThreadsForSubreddits(subreddit, argDict):
    print("Processing subreddit: %s" % (subreddit.name))

    # create PRAW reddit instance
    reddit = praw.Reddit(client_id=CONST_CLIENT_ID, client_secret=CONST_SECRET, user_agent=CONST_USER_AGENT, username=CONST_DEV_USERNAME, password=CONST_DEV_PASSWORD)

    # get status of comments already processed by this subreddit
    params={};
    cs = getSubredditThreadProcessedStatus(subreddit)
    # NOTE: Not using youngest currently because using it:
    #       * limits resuilts to 100 for some reason
    #       * fails if youngest doesn't exist any more (or is too old)
    # if cs.youngest != "":
    #     params['before'] = cs.youngest;

    # iterate through submissions saving them
    countNew = 0
    countDuplicate = 0
    for thread in reddit.subreddit(subreddit.name).new(limit=1023, params=params):
        aDict = {'sti' : None, 'isNew' : True }
        getSubredditThreadIndex(thread, subreddit, aDict)

        if aDict['isNew']:
            saveSubredditThreadRaw(thread, aDict['sti'])
            countNew += 1
        else:
            countDuplicate += 1

        # update youngest appropriately
        if thread.name > cs.youngest:
            cs.youngest = thread.name

    # save cs so it contains appropriate value for youngest
    cs.save()

    argDict['rv'] += "<br><b>" + subreddit.name + "</b>: " + str(countNew) + " new and " + str(countDuplicate) + " duplicate submissions processed"
    return

# *****************************************************************************
def threads_updateForAllSubreddits():
    print("=====================================================")
    rv = "<B>PRAW</B> threads_updateForAllSubreddits<BR>"

    subreddits = subreddit.objects.all()
    if subreddits.count() == 0:
        rv += "<BR> No subreddits found"
    else:
        for su in subreddits:
            argDict = {'rv': ""}
            updateThreadsForSubreddits(su, argDict)
            rv += argDict['rv']
    print("=====================================================")
    return HttpResponse(rv)






































