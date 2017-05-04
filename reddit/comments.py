from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import user, userCommentsProcessedStatus, userCommentsIndex, userCommentsRaw
from redditCommon.constants import *
# from redditCommon.credentials import credentials_getAuthorizationHeader
# from redditCommon.listingDict import *
import json
# import requests
import praw
import pprint

# # *****************************************************************************
# def displayCommentListingDataChildren(d):
#     rv = ""
#     if 'children' in d['data']:
#         count = 0
#         for cd in d['data']['children']:
#             count += 1
#             rv += "<BR><b>" + str(count) + ": " + cd['data']['name'] + "</b> " + cd['data']['body']
#     return rv;

# # *****************************************************************************
# def processCommentListingCreatingIndexAndRawEntriesAppropriately(d, u):
#     youngestChild = ""
#     count = 0
#     for cd in d['data']['children']:
#         if cd['data']['name'] > youngestChild:
#             youngestChild = cd['data']['name']
#
#         count += 1
#
#         # see if userCommentsIndex exists, create if necessary
#         uc = None
#         try:
#             uc = userCommentsIndex.objects.get(user=u, name=cd['data']['name'])
#             s = "WARNING: userCommentsIndex: " + uc.name + " already exists"
#             print(s)
#         except ObjectDoesNotExist:
#             uc = userCommentsIndex(user=u, name=cd['data']['name'])
#             uc.save()
#
#         # see if userCommentsRaw exists, create if necessary
#         ucr = None
#         try:
#             ucr = userCommentsRaw.objects.get(uci=uc)
#             s = "WARNING: userCommentsRaw: " + ucr.uci.name + " for user " + ucr.uci.user.name + " already exists"
#             print(s)
#         except ObjectDoesNotExist:
#             ucr = userCommentsRaw(uci=uc, data=cd['data'])
#             ucr.save()
#
#     print ("*** %s comments retrieved" % (str(count)))
#     return youngestChild;

# # *****************************************************************************
# def buildCommentQuery(name, after, before):
#     rv = CONST_REDDIT_USER_COMMENT_REQUEST_URL
#     rv += name
#     rv += '/comments'
#     rv += '/.json?limit='
#     rv += str(CONST_REDDIT_REQUEST_LIMIT)
#
#     if after == CONST_UNPROCESSED:
#         pass
#     elif after != CONST_PROCESSED:
#         rv += '&after=' + after
#     else:
#         if before == CONST_UNPROCESSED:
#             pass
#         elif before != CONST_PROCESSED:
#             rv += '&before=' + before
#         else:
#             pass
#
#     return rv

# # *****************************************************************************
# def getDictOfNewCommentsForUser(cs, d):
#     rv = "<BR>" + cs.user.name + ": AA: " + "[After: " + cs.after + "]" + " [Before: " + cs.before + "]"
#     # EXAMPLE: UserName: AA: [After: processed] [Before: t1_dddddd86]
#
#     commentQuery = buildCommentQuery(cs.user.name, cs.after, cs.before)
#     rv += "<BR>commentQuery: " + commentQuery
#     # EXAMPLE: commentQuery: https://oauth.reddit.com/user/OldDevLearningLinux/comments/.json?limit=100&before=t1_dejemg4
#
#     AuthHeader = credentials_getAuthorizationHeader()
#     # print ("*** %s" % (json.dumps(AuthHeader)))
#     # EXAMPLE: {"User-Agent": "testscript by /u/OldDevLearningLinux", "Authorization": "bearer eAKTo07KQutnf1qCMBNphzuU9Wg"}
#
#     r = requests.get(commentQuery, headers=AuthHeader)
#     d.update(r.json())
#
#     return rv

# *****************************************************************************
# get userCommentsProcessedStatus for user, if not exist create on
def getUsersCommentsProcessedStatus(u):
    cs = None
    try:
        cs = userCommentsProcessedStatus.objects.get(user=u)
    except ObjectDoesNotExist:
        cs = userCommentsProcessedStatus(user=u)
        cs.save()
    return cs


# # *****************************************************************************
# def processCommentListingCreatingIndexAndRawEntriesAppropriately(d, u):
#     youngestChild = ""
#     count = 0
#     for cd in d['data']['children']:
#         if cd['data']['name'] > youngestChild:
#             youngestChild = cd['data']['name']
#
#         count += 1
#

#
#         # see if userCommentsRaw exists, create if necessary
#         ucr = None
#         try:
#             ucr = userCommentsRaw.objects.get(uci=uc)
#             s = "WARNING: userCommentsRaw: " + ucr.uci.name + " for user " + ucr.uci.user.name + " already exists"
#             print(s)
#         except ObjectDoesNotExist:
#             ucr = userCommentsRaw(uci=uc, data=cd['data'])
#             ucr.save()
#
#     print ("*** %s comments retrieved" % (str(count)))
#     return youngestChild;

# *****************************************************************************
# if userCommentsIndex exists return it otherwise create it
def getUserCommentIndex(comment, u):
    uci = None
    try:
        uci = userCommentsIndex.objects.get(user=u, name=comment.name)
        print ("WARNING: getUserCommentIndex: " + uci.name + " already exists");
    except ObjectDoesNotExist:
        uci = userCommentsIndex(user=u, name=comment.name)
        uci.save()
    return uci


# *****************************************************************************
# if saveUserCommentsRaw does not exist save it.
# TODO else compare appropriate fields, if any differences record appropriately
def saveUserCommentsRaw(comment, uci):
    ucr = None
    try:
        ucr = userCommentsRaw.objects.get(uci=uci)
        print("WARNING: saveUserCommentsRaw: " + ucr.uci.name + " for user " + ucr.uci.user.name + " already exists")
    except ObjectDoesNotExist:
        # vars converts comment to json dict which can be saved to DB
        ucr = userCommentsRaw(uci=uci, data=vars(comment))
        ucr.save()

    return

# *****************************************************************************
def updateCommentsForUser(u, argDict):
    print("Processing user: %s" % (u.name))

    # create PRAW reddit instance
    reddit = praw.Reddit(client_id=CONST_CLIENT_ID, client_secret=CONST_SECRET, user_agent=CONST_USER_AGENT, username=CONST_DEV_USERNAME, password=CONST_DEV_PASSWORD)

    # get status of comments already processed by this user
    cs = getUsersCommentsProcessedStatus(u)
    params={};
    if cs.youngest != "":
        params['before'] = cs.youngest;

    # iterate through comments saving them
    count = 0
    for comment in reddit.redditor(u.name).comments.new(limit=None, params=params):
        uci = getUserCommentIndex(comment, u)
        saveUserCommentsRaw(comment, uci)
        # update youngest appropriately
        if comment.name > cs.youngest:
            cs.youngest = comment.name
        count += 1

    # save cs so it contains appropriate value for youngest
    cs.save()

    argDict['rv'] += "<br><b>" + u.name + "</b>: " + str(count) + " comments processed."
    return

# *****************************************************************************
def comments_updateForAllUsers():
    print("=====================================================")
    rv = "<B>PRAW</B> comments_updateForAllUsers<BR>"

    users = user.objects.filter(poi=True)
    if users.count() == 0:
        rv += "<BR> No users found"
    else:
        for u in users:
            argDict = {'rv': ""}
            updateCommentsForUser(u, argDict)
            rv += argDict['rv']
    print("=====================================================")
    return HttpResponse(rv)




















