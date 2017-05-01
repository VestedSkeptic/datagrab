from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
# from .models import user, userCommentsProcessedStatus, userCommentsIndex, userCommentsRaw
from .models import subreddit, subredditThreadProcessedStatus, subredditThreadIndex, subredditThreadRaw
from .defines import *
from .credentials import credentials_getAuthorizationHeader
from helperLibrary.stringHelper import *
import requests, json

# *****************************************************************************
CONST_REDDIT_REQUEST_URL    = "https://oauth.reddit.com/r/"
CONST_REDDIT_REQUEST_LIMIT  = 100
# CONST_REDDIT_REQUEST_LIMIT  = 2

# commentQuery: https://oauth.reddit.com/user/OldDevLearningLinux/comments/.json?limit=100&before=t1_dejemg4
# threadQuery:  https://oauth.reddit.com/r/politics/new/.json?limit=100

# CONST_THREAD_RETRIEVAL_MODE = "hot"
# CONST_THREAD_RETRIEVAL_MODE = "rising"
CONST_THREAD_RETRIEVAL_MODE = "new"

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
    return rv;

# *****************************************************************************
def processThreadListingCreatingIndexAndRawEntriesAppropriately(d, sr):
    youngestChild = ""
    count = 0
    # if 'children' in d['data']:
    for cd in d['data']['children']:
        if cd['data']['name'] > youngestChild:
            youngestChild = cd['data']['name']

        count += 1

        # see if subredditThreadIndex exists, create if necessary
        st = None
        try:
            st = subredditThreadIndex.objects.get(subreddit=sr, name=cd['data']['name'])
            s = "WARNING: subredditThreadIndex: " + st.name + " already exists"
            print(s)
        except ObjectDoesNotExist:
            st = subredditThreadIndex(subreddit=sr, name=cd['data']['name'])
            st.save()
            # s = "subredditThreadIndex: " + st.name + " created"
            # print(s)

        # see if subredditThreadRaw exists, create if necessary
        stRaw = None
        try:
            stRaw = subredditThreadRaw.objects.get(sti=st)
            s = "WARNING: subredditThreadRaw: " + stRaw.sti.name + " for thread " + stRaw.sti.subreddit.name + " already exists"
            print(s)
        except ObjectDoesNotExist:
            # stRaw = subredditThreadRaw(sti=st, data=cd['data'])
            stRaw = subredditThreadRaw(sti=st, data=cd['data'], title=cd['data']['title'])
            stRaw.save()
            # s = "subredditThreadRaw: " + stRaw.uci.name + " created"
            # print(s)

    print ("*** %s threads retrieved" % (str(count)))
    return youngestChild;

# *****************************************************************************
def buildThreadQuery(name, after, before):
    rv = CONST_REDDIT_REQUEST_URL
    rv += name
    rv += '/'
    rv += CONST_THREAD_RETRIEVAL_MODE
    # rv += '/.json?limit=100'
    rv += '/.json?limit='
    rv += str(CONST_REDDIT_REQUEST_LIMIT)

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
def validateNewThreadsDataDict (d, argDict):
    if 'message' in d:
        argDict['rv'] += displayMessageFromDict(d)
    elif 'data' in d:
        if 'children' in d['data']:
            argDict['validateResult'] = True
            argDict['rv'] += "<BR>VALIDATES SUCCESSFULLY"
        else:
            argDict['rv'] += "<BR>ERROR: children key not found in d[data]"
    else:
        argDict['rv'] += displayUnknownDict(d)
    return

# *****************************************************************************
def getDictOfNewThreadsForSubreddit(cs, d):
    rv = "<BR>" + cs.subreddit.name + ": AA: " + "[After: " + cs.after + "]" + " [Before: " + cs.before + "]"
    # EXAMPLE: politics: AA: [After: NOT processed] [Before: NOT processed]

    threadQuery = buildThreadQuery(cs.subreddit.name, cs.after, cs.before)
    rv += "<BR>threadQuery: " + threadQuery
    # EXAMPLE: threadQuery: https://oauth.reddit.com/r/politics/new/.json?limit=100

    AuthHeader = credentials_getAuthorizationHeader()
    # print ("*** %s" % (json.dumps(AuthHeader)))
    # EXAMPLE: {"User-Agent": "testscript by /u/OldDevLearningLinux", "Authorization": "bearer eAKTo07KQutnf1qCMBNphzuU9Wg"}

    r = requests.get(threadQuery, headers=AuthHeader)
    d.update(r.json())

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
def updateThreadsForSubreddit(s):
    rv = "<BR> ---------------------------------"
    print ("Processing subreddit: %s" % (s.name))
    cs = getSubredditThreadProcessedStatus(s)

    # rv += getNewThreadsForSubreddit(cs)
    d = {}
    rv += getDictOfNewThreadsForSubreddit(cs, d)
    # print ("*** %s" % (json.dumps(d)))

    argDict = {'rv': "", 'validateResult': False}
    validateNewThreadsDataDict(d, argDict)
    rv += argDict['rv']

    if argDict['validateResult']:
        print("*** validate is true")

        rv += displayThreadListingDictMeta(d)
        # EXAMPLE: THREAD DATA: AFTER: t3_68g9dd, BEFORE: None, MODHASH: , CHILDREN: 100

        rv += displayThreadListingDataChildren(d)
        # EXAMPLE: 1: t3_68gzts Trump's chief of staff: 'We've looked at' changing libel laws

        youngestChild = processThreadListingCreatingIndexAndRawEntriesAppropriately(d, cs.subreddit)

        rv += "<BR>youngestChild = " + youngestChild
        # EXAMPLE: youngestChild = t1_dgy8eac

        if youngestChild > cs.before:
            cs.before = youngestChild

        if d['data']['after'] is not None:
            cs.after = d['data']['after']
        else:
            cs.after = CONST_PROCESSED
        cs.save()
    else:
        print("*** validate is false")

    rv += "<BR>" + cs.subreddit.name + ": BB: " + "[After: " + cs.after + "]" + " [Before: " + cs.before + "]"
    # EXAMPLE: politics: BB: [After: NOT processed] [Before: NOT processed]

    rv += "<br>"
    print("")
    return rv

# *****************************************************************************
def threads_updateForAllSubreddits():
    rv = "<B>threads_updateForAllSubreddits</B><BR>"
    print("=====================================================")

    subreddits = subreddit.objects.all()
    if subreddits.count() == 0:
        rv += "<BR> ---------------------------------"
        rv += "<BR> No subreddits found"
    else:
        for s in subreddits:
            rv += updateThreadsForSubreddit(s)
    return HttpResponse(rv)























