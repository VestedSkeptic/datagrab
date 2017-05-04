from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import subreddit, subredditThreadProcessedStatus, subredditThreadIndex, subredditThreadRaw
from redditCommon.constants import *
from redditCommon.credentials import credentials_getAuthorizationHeader
from redditCommon.listingDict import *
import requests, json
import praw
import pprint

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

        # see if subredditThreadRaw exists, create if necessary
        stRaw = None
        try:
            stRaw = subredditThreadRaw.objects.get(sti=st)
            s = "WARNING: subredditThreadRaw: " + stRaw.sti.name + " for thread " + stRaw.sti.subreddit.name + " already exists"
            print(s)
        except ObjectDoesNotExist:
            stRaw = subredditThreadRaw(sti=st, data=cd['data'], title=cd['data']['title'])
            stRaw.save()

    print ("*** %s threads retrieved" % (str(count)))
    return youngestChild;

# *****************************************************************************
def buildThreadQuery(name, after, before):
    rv = CONST_REDDIT_SUBREDDIT_THREAD_REQUEST_URL
    rv += name
    rv += '/'
    rv += CONST_REDDIT_SUBREDDIT_THREAD_REQUEST_RETRIEVAL_MODE
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
    listingDict_validate(d, argDict)
    rv += argDict['rv']

    if argDict['validateResult']:
        print("*** validate is true")

        rv += listingDict_displayMeta(d)
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
def hack_doInitialCallToGetMostCommentsForAThread():
    rv = "";

    # threadQuery = "https://oauth.reddit.com/r/test/comments/68uvd9/.json?sort=old&threaded=false&limit=5"
    threadQuery = "https://oauth.reddit.com/r/test/comments/68uvd9/.json?sort=old&threaded=false&limit=1"
    rv += "<BR>threadQuery: " + threadQuery + "<br>"

    AuthHeader = credentials_getAuthorizationHeader()
    r = requests.get(threadQuery, headers=AuthHeader)

    print (r.json())
    # d.update(r.json())
    # rv += r.json()

    rv += json.dumps(r.json())

    return rv;


# *****************************************************************************
def hack_doSecondCallToGetMoreChildrenForAThread():
    rv = "";

    # threadQuery = "https://oauth.reddit.com/api/morechildren/.json?api_type=json&sort=new&link_id=t3_68uvd9&children=dh1g4v6,dh1g58x"
    # rv += "<BR>threadQuery: " + threadQuery + "<br>"
    # AuthHeader = credentials_getAuthorizationHeader()
    # r = requests.get(threadQuery, headers=AuthHeader)

    # OR TRYING WITH POST

    payload = {'sort': 'new', 'link_id': 't3_68uvd9', 'api_type' : 'json', 'children' : 'dh1g4v6,dh1g58x', }
    threadQuery = "https://oauth.reddit.com/api/morechildren/.json"
    rv += "<BR>threadQuery: " + threadQuery + "<br>"
    AuthHeader = credentials_getAuthorizationHeader()
    r = requests.post(threadQuery, headers=AuthHeader, data=payload)






    print (r.json())
    # d.update(r.json())
    # rv += r.json()

    rv += json.dumps(r.json())

    return rv;


# # *****************************************************************************
# def threadComments_updateForAll():
#     rv = "<B>subredditComments_updateForAllSubreddits</B><BR>"
#     print("=====================================================")
#
#     # rv += hack_doInitialCallToGetMostCommentsForAThread()
#
#     rv += hack_doSecondCallToGetMoreChildrenForAThread()
#
#     # subreddits = subreddit.objects.all()
#     # if subreddits.count() == 0:
#     #     rv += "<BR> ---------------------------------"
#     #     rv += "<BR> No subreddits found"
#     # else:
#     #     for s in subreddits:
#     #         rv += updateThreadsForSubreddit(s)
#     return HttpResponse(rv)


# *****************************************************************************
def threadComments_updateForAll():
    rv = "<B>subredditComments_updateForAllSubreddits</B><BR>"
    print("=====================================================")


    reddit = praw.Reddit(
        client_id=CONST_CLIENT_ID,
        client_secret=CONST_SECRET,
        user_agent=CONST_USER_AGENT,
        username=CONST_DEV_USERNAME,
        password=CONST_DEV_PASSWORD)

    # # subreddit = reddit.subreddit('redditdev')
    # #
    # # print(subreddit.display_name)  # Output: redditdev
    # # # print(subreddit.title)         # Output: reddit Development
    # # # print(subreddit.description)   # Output: A subreddit for discussion of
    # #
    # #
    # # for submission in subreddit.hot(limit=10):
    # #     print(submission.title)  # Output: the submission's title
    # #     # print(submission.score)  # Output: the submission's score
    # #     print(submission.id)     # Output: the submission's ID
    # #     # print(submission.url)    # Output: the URL the submission points to
    # #     #                          # or the submission's URL if it's a self post
    #
    #
    #
    # # for comment in reddit.redditor('OldDevLearningLinux').comments.new(limit=None):
    # count = 0
    # # redditUser = 'OldDevLearningLinux'
    # # redditUser = 'roadsideBandit'
    # redditUser = 'stp2007'
    # # # for comment in reddit.redditor(redditUser).comments.new(limit=None):
    # # for comment in reddit.redditor(redditUser).comments.new(limit=1):
    # #     count += 1
    # #
    # #     # determine attributes available in object
    # #     print(comment.name) # to make it non-lazy
    # #     pprint.pprint(vars(comment))
    #
    #
    # # comment = reddit.redditor('stp2007').comments.new(limit=1).next()
    # # print(comment.name) # to make it non-lazy
    # # pprint.pprint(vars(comment))
    #
    # subreddit = reddit.subreddit('redditdev')
    # submission = subreddit.hot(limit=1).next()
    # print(submission.title)  # to make it non-lazy
    # pprint.pprint(vars(submission))






    # for comment in reddit.redditor('OldDevLearningLinux').comments.new(limit=None):
    count = 0
    redditUser = 'OldDevLearningLinux'
    # redditUser = 'roadsideBandit'
    # redditUser = 'stp2007'
    # for comment in reddit.redditor(redditUser).comments.new(limit=None):
    for comment in reddit.redditor(redditUser).comments.new(limit=5):
        count += 1
        print("CALL 1: %d: %s: %s" % (count, comment.id, comment.body.split('\n', 1)[0][:79]))

    print("----------------------")
    for comment in reddit.redditor(redditUser).comments.new(limit=2, params={"before" : "t1_dh2oxc9"}):
        count += 1
        print("CALL 2: %d: %s: %s" % (count, comment.id, comment.body.split('\n', 1)[0][:79]))

    # print("----------------------")
    # for comment in reddit.redditor(redditUser).comments.new(limit=3, params={"after" : "t1_dh2oxc9"}):
    #     count += 1
    #     print("CALL 3: %d: %s: %s" % (count, comment.id, comment.body.split('\n', 1)[0][:79]))
    #
    # print("----------------------")
    # for comment in reddit.redditor(redditUser).comments.new(limit=4, params={"after" : "dh2oxc9"}):
    #     count += 1
    #     print("CALL 4: %d: %s: %s" % (count, comment.id, comment.body.split('\n', 1)[0][:79]))




# https://www.reddit.com/user/OldDevLearningLinux/
# https://www.reddit.com/user/OldDevLearningLinux/comments/?before=t1_dh2oxc9
#
# # https://www.reddit.com/r/redditdev/comments/68w9x7/morechildren_api_results_not_consistent/dh2oxc9/
#
# # len(list(reddit.redditor('bboe').comments.new(limit=None, params={'before': 't1_dh2tczt'})))
# # Out[5]: 1



# IF SAVING RAW INDICATE SOURCE FOR RAW ITEM
# THEREFORE COMMENTS CAN HAVE TWO SOURCES.
# ONE DIRECTLY FROM A REDDIT USERNAME
# ANOTHER FROM FOLLOWING A SUBMISSION REPLIES
# TRACKING SOURCE MIGHT HELP WITH SLIGHLY DIFFERENT FIELDS
# RETURNED BY DIFFERENT SOURCES











    print("=====================================================")

    return HttpResponse(rv)
























