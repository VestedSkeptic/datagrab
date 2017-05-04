from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import subreddit, subredditThreadProcessedStatus, subredditThreadIndex, subredditThreadRaw
from redditCommon.constants import *
import json
# import pprint



# *****************************************************************************
def threads_updateForAllSubreddits():
    print("=====================================================")
    rv = "<B>threads_updateForAllSubreddits</B><BR>"

    # subreddits = subreddit.objects.all()
    # if subreddits.count() == 0:
    #     rv += "<BR> No subreddits found"
    # else:
    #     for s in subreddits:
    #         argDict = {'rv': ""}
    #         updateThreadsForSubreddit(s, argDict)
    #         rv += argDict['rv']

    print("=====================================================")
    return HttpResponse(rv)

















