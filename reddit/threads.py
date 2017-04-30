from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
# from .models import user, userCommentsProcessedStatus, userCommentsIndex, userCommentsRaw
from .models import subreddit, subredditThreadProcessedStatus
from .defines import *
from .credentials import credentials_getAuthorizationHeader
from helperLibrary.stringHelper import *
import requests, json

# *****************************************************************************
# CONST_REDDIT_REQUEST_URL    = "https://www.reddit.com/user/"
# CONST_REDDIT_REQUEST_URL    = "https://oauth.reddit.com/user/"
CONST_REDDIT_REQUEST_URL    = "https://oauth.reddit.com/r/"


# commentQuery: https://oauth.reddit.com/user/OldDevLearningLinux/comments/.json?limit=100&before=t1_dejemg4
# threadQuery:  https://oauth.reddit.com/r/politics/new/.json?limit=100


# CONST_THREAD_RETRIEVAL_MODE = "hot"
CONST_THREAD_RETRIEVAL_MODE = "new"
# CONST_THREAD_RETRIEVAL_MODE = "rising"

# *****************************************************************************
def displayMessageFromDict(d):
    rv = "<BR>ERROR MESSAGE: " + d['message']
    if 'error' in d:
        rv += ", " + "ERROR: " + str(d['error'])
    return rv

# *****************************************************************************
def displayUnknownDict(d):
    rv = "<BR>ERROR UNKNOWN: " + json.dumps(d)
    return rv

# *****************************************************************************
def displayThreadListingDictMeta(d):
    rv = ""
    # rv = "<br>KIND: "
    # if 'kind' in d: rv += d['kind']
    # else:           rv += "ERROR kind NOT FOUND"

    if 'data' in d:
        rv += "<br>THREAD DATA: "
        if 'after' in d['data']:    rv += "AFTER: "       + stringHelper_returnStringValueOrNone(d['data']['after'])   + ", "
        if 'before' in d['data']:   rv += "BEFORE: "      + stringHelper_returnStringValueOrNone(d['data']['before'])  + ", "
        if 'modhash' in d['data']:  rv += "MODHASH: "     + stringHelper_returnStringValueOrNone(d['data']['modhash']) + ", "
        if 'children' in d['data']: rv += "CHILDREN: "    + str(len(d['data']['children']))
    else:
        rv += "ERROR data NOT FOUND"
    return rv

# *****************************************************************************
def displayThreadListingDataChildren(d):
    rv = ""
    if 'children' in d['data']:
        count = 0
        for cd in d['data']['children']:
            count += 1
            rv += "<BR><b>" + str(count) + ": " + cd['data']['name'] + "</b> " + cd['data']['title']
            # rv += "<BR>" + json.dumps(cd['data'])
            break
    return rv;

# *****************************************************************************
def processCommentListingDataChildren(d, u):
    youngestChild = ""
    count = 0
    if 'children' in d['data']:
        for cd in d['data']['children']:
            if cd['data']['name'] > youngestChild:
                youngestChild = cd['data']['name']

            count += 1

            # see if userCommentsIndex exists, create if necessary
            uc = None
            try:
                uc = userCommentsIndex.objects.get(user=u, name=cd['data']['name'])
                s = "WARNING: userCommentsIndex: " + uc.name + " already exists"
                print(s)
            except ObjectDoesNotExist:
                uc = userCommentsIndex(user=u, name=cd['data']['name'])
                uc.save()
                # s = "userCommentsIndex: " + uc.name + " created"
                # print(s)

            # see if userCommentsRaw exists, create if necessary
            ucr = None
            try:
                ucr = userCommentsRaw.objects.get(uci=uc)
                s = "WARNING: userCommentsRaw: " + ucr.uci.name + " for user " + ucr.uci.user.name + " already exists"
                print(s)
            except ObjectDoesNotExist:
                ucr = userCommentsRaw(uci=uc, data=cd['data'])
                ucr.save()
                # s = "userCommentsRaw: " + ucr.uci.name + " created"
                # print(s)

    print ("*** %s comments retrieved" % (str(count)))

    return youngestChild;

# *****************************************************************************
def buildThreadQuery(name, after, before):
    rv = CONST_REDDIT_REQUEST_URL
    rv += name
    rv += '/'
    rv += CONST_THREAD_RETRIEVAL_MODE
    rv += '/.json?limit=100'

    if after == CONST_UNPROCESSED:
        pass
    elif after != CONST_PROCESSED:
        rv += '&after=' + after
    else:
        if before == CONST_UNPROCESSED:
            pass
        elif before != CONST_PROCESSED:
            rv += '&before=' + before
        else:
            pass

    return rv

# *****************************************************************************
def getNewThreadsForSubreddit(cs):
    rv = "<BR>" + cs.subreddit.name + ": AA: " + "[After: " + cs.after + "]" + " [Before: " + cs.before + "]"
    # EXAMPLE: politics: AA: [After: NOT processed] [Before: NOT processed]

    threadQuery = buildThreadQuery(cs.subreddit.name, cs.after, cs.before)
    rv += "<BR>threadQuery: " + threadQuery
    # EXAMPLE: threadQuery: https://oauth.reddit.com/r/politics/new/.json?limit=100

    AuthHeader = credentials_getAuthorizationHeader()
    # print ("*** %s" % (json.dumps(AuthHeader)))
    # EXAMPLE: {"User-Agent": "testscript by /u/OldDevLearningLinux", "Authorization": "bearer eAKTo07KQutnf1qCMBNphzuU9Wg"}

    r = requests.get(threadQuery, headers=AuthHeader)
    d = r.json()
    ##### EVENTUALLY CHANGE TO     d.update(r.json())  WHEN D IS PASSED IN VIA A PARAMETER

    if 'message' in d:
        rv += displayMessageFromDict(d)
    elif 'data' in d:
        rv += displayThreadListingDictMeta(d)
        # EXAMPLE: THREAD DATA: AFTER: t3_68g9dd, BEFORE: None, MODHASH: , CHILDREN: 100

        rv += displayThreadListingDataChildren(d)
        # EXAMPLE: 1: t3_68gzts Trump's chief of staff: 'We've looked at' changing libel laws

        # youngestChild = processCommentListingDataChildren(d, cs.user)
        # rv += "<BR>youngestChild = " + youngestChild
        #
        # if youngestChild > cs.before:
        #     cs.before = youngestChild
        #
        # if d['data']['after'] is not None:
        #     cs.after = d['data']['after']
        # else:
        #     cs.after = CONST_PROCESSED
        # cs.save()
    else:
        rv += displayUnknownDict(d)

    rv += "<BR>" + cs.subreddit.name + ": BB: " + "[After: " + cs.after + "]" + " [Before: " + cs.before + "]"
    # EXAMPLE: politics: BB: [After: NOT processed] [Before: NOT processed]
    return rv

# *****************************************************************************
def getSubredditThreadProcessedStatus(s):
    # get subredditThreadProcessedStatus for subreddit, if not exist create one
    ts = None
    try:
        ts = subredditThreadProcessedStatus.objects.get(subreddit=s)
        print("*** subredditThreadProcessedStatus already exists")
    except ObjectDoesNotExist:
        ts = subredditThreadProcessedStatus(subreddit=s)
        ts.save()
        print("*** subredditThreadProcessedStatus created")
    return ts

# *****************************************************************************
def threads_updateForAllSubreddits():
    rv = "<B>threads_updateForAllSubreddits</B><BR>"
    print("=====================================================")

    subreddits = subreddit.objects.all()
    count = 0
    for s in subreddits:
        count += 1
        rv += "<BR> ---------------------------------"
        rv += "<BR>" + s.name + ":"
        print ("Processing subreddit: %s" % (s.name))
        cs = getSubredditThreadProcessedStatus(s)
        rv += getNewThreadsForSubreddit(cs)
        rv += "<br>"
        print("")

    if count == 0:
        rv += "<BR> ---------------------------------"
        rv += "<BR> No subreddits found"

    return HttpResponse(rv)























