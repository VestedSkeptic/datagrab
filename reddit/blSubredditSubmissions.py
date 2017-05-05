from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import subreddit, subredditSubmissionIndex, subredditSubmissionRaw
from .constants import *
import json
import praw
import pprint

# *****************************************************************************
# if subredditSubmissionIndex exists return it otherwise create it
def blSubredditSubmissions_getsubredditSubmissionIndex(submission, subreddit, aDict):
    sti = None
    try:
        sti = subredditSubmissionIndex.objects.get(subreddit=subreddit, name=submission.name)
        aDict['isNew'] = False
    except ObjectDoesNotExist:
        sti = subredditSubmissionIndex(subreddit=subreddit, name=submission.name, iidd=submission.id)
        sti.save()
    aDict['sti'] = sti
    return

# *****************************************************************************
# if subredditSubmissionRaw does not exist save it.
# TODO else compare appropriate fields, if any differences record appropriately
def blSubredditSubmissions_savesubredditSubmissionRaw(submission, sti):
    stRaw = None
    try:
        stRaw = subredditSubmissionRaw.objects.get(sti=sti)
    except ObjectDoesNotExist:
        # vars converts submission to json dict which can be saved to DB
        stRaw = subredditSubmissionRaw(sti=sti, data=vars(submission), title=submission.title)
        stRaw.save()
    return

# *****************************************************************************
def blSubredditSubmissions_updateThreadsForSubreddits(subreddit, argDict):
    print("Processing subreddit: %s" % (subreddit.name))

    # create PRAW reddit instance
    reddit = praw.Reddit(client_id=CONST_CLIENT_ID, client_secret=CONST_SECRET, user_agent=CONST_USER_AGENT, username=CONST_DEV_USERNAME, password=CONST_DEV_PASSWORD)

    # get youngest subredditSubmissionIndex in DB if there are any
    params={};
    youngest = ''
    qs = subredditSubmissionIndex.objects.filter(subreddit=subreddit).order_by('-name')
    if qs.count() > 0:
        youngest = qs[0].name
    # print ("youngest = %s" % youngest)



    # get status of comments already processed by this subreddit
    # NOTE: Not using youngest currently because using it:
    #       * limits resuilts to 100 for some reason
    #       * fails if youngest doesn't exist any more (or is too old)
    # if cs.youngest != "":
    #     params['before'] = cs.youngest;

    # iterate through submissions saving them
    countNew = 0
    countDuplicate = 0
    for submission in reddit.subreddit(subreddit.name).new(limit=None, params=params):
        aDict = {'sti' : None, 'isNew' : True }
        blSubredditSubmissions_getsubredditSubmissionIndex(submission, subreddit, aDict)

        if aDict['isNew']:
            blSubredditSubmissions_savesubredditSubmissionRaw(submission, aDict['sti'])
            countNew += 1
        else:
            countDuplicate += 1

    argDict['rv'] += "<br><b>" + subreddit.name + "</b>: " + str(countNew) + " new and " + str(countDuplicate) + " duplicate submissions processed"
    return

# *****************************************************************************
def blSubredditSubmissions_updateForAllSubreddits():
    print("=====================================================")
    rv = "<B>PRAW</B> blSubredditSubmissions_updateForAllSubreddits<BR>"

    subreddits = subreddit.objects.all()
    if subreddits.count() == 0:
        rv += "<BR> No subreddits found"
    else:
        for su in subreddits:
            argDict = {'rv': ""}
            blSubredditSubmissions_updateThreadsForSubreddits(su, argDict)
            rv += argDict['rv']
    print("=====================================================")
    return HttpResponse(rv)






































