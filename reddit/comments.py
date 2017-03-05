from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import user, commentStatus
from .defines import *
from .credentials import credentials_getAuthorizationHeader
from helperLibrary.stringHelper import *
import requests, json

# *****************************************************************************
# CONST_REDDIT_REQUEST_URL    = "https://www.reddit.com/user/"
CONST_REDDIT_REQUEST_URL    = "https://oauth.reddit.com/user/"

# *****************************************************************************
def displayMessageFromDict(d):
    rv = "MESSAGE: " + d['message']
    if 'error' in d:
        rv += ", " + "ERROR: " + str(d['error'])
    return rv

# *****************************************************************************
def displayUnknownDict(d):
    rv = "UNKNOWN: " + json.dumps(d)
    return rv

# *****************************************************************************
def displayCommentListingDictMeta(d):
    rv = ""
    # rv = "<br>KIND: "
    # if 'kind' in d: rv += d['kind']
    # else:           rv += "ERROR kind NOT FOUND"

    if 'data' in d:
        rv += "<br>DATA: "
        if 'after' in d['data']:    rv += "AFTER: "       + stringHelper_returnStringValueOrNone(d['data']['after'])   + ", "
        if 'before' in d['data']:   rv += "BEFORE: "      + stringHelper_returnStringValueOrNone(d['data']['before'])  + ", "
        if 'modhash' in d['data']:  rv += "MODHASH: "     + stringHelper_returnStringValueOrNone(d['data']['modhash']) + ", "
        if 'children' in d['data']: rv += "CHILDREN: "    + str(len(d['data']['children']))
    else:
        rv += "ERROR data NOT FOUND"
    return rv

# # *****************************************************************************
# def processCommentListingDataChildren(d):
#     rv = "<br>"
#     if 'children' in d['data']:
#         count = 0
#         for cd in d['data']['children']:
#             count += 1
#             rv += "<BR><b>" + str(count) + " " + cd['data']['name'] + "</b> " + cd['data']['body']
#     return rv;

# *****************************************************************************
def displayCommentListingDataChildren(d):
    rv = ""
    if 'children' in d['data']:
        count = 0
        for cd in d['data']['children']:
            count += 1
            rv += "<BR><b>" + str(count) + ": " + cd['data']['name'] + "</b> " + cd['data']['body']
    return rv;

# *****************************************************************************
def processCommentListingDataChildren(d):
    youngestChild = ""
    if 'children' in d['data']:
        for cd in d['data']['children']:
            if cd['data']['name'] > youngestChild:
                youngestChild = cd['data']['name']
    return youngestChild;

# *****************************************************************************
def buildCommentQuery(name, after, before):
    rv = CONST_REDDIT_REQUEST_URL
    rv += name
    rv += '/comments/.json?limit=100'

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
# def requestCommentsForUser(redditusername, after):
def requestCommentsForUser(cs):
    rv = ""

    commentQuery = buildCommentQuery(cs.user.name, cs.after, cs.before)
    rv += "<BR>commentQuery: " + commentQuery

    AuthHeader = credentials_getAuthorizationHeader()
    print (json.dumps(AuthHeader))

    r = requests.get(commentQuery, headers=AuthHeader)
    d = r.json()

    if 'message' in d:
        rv += displayMessageFromDict(d)
    elif 'data' in d:
        rv += displayCommentListingDictMeta(d)
        rv += displayCommentListingDataChildren(d)
        youngestChild = processCommentListingDataChildren(d)
        rv += "<BR>youngestChild = " + youngestChild

        if youngestChild > cs.before:
            cs.before = youngestChild

        if d['data']['after'] is not None:
            cs.after = d['data']['after']
        else:
            cs.after = CONST_PROCESSED
        cs.save()
    else:
        rv += displayUnknownDict(d)
    return rv

# *****************************************************************************
def pullCommentsForUser(u):
    # get commentStatus for user, if not exist create one
    cs = None
    try:
        cs = commentStatus.objects.get(user=u)
    except ObjectDoesNotExist:
        cs = commentStatus(user=u)
        cs.save()
    rv = "<BR>" + u.name + ": AA: " + "[After: " + cs.after + "]" + " [Before: " + cs.before + "]"
    rv += requestCommentsForUser(cs)
    rv += "<BR>" + u.name + ": BB: " + "[After: " + cs.after + "]" + " [Before: " + cs.before + "]"

    return rv

# *****************************************************************************
def comments_updateForAllUsers():
    rv = ""
    users = user.objects.all()
    for u in users:
        rv += "<BR>" + u.name + ":"
        rv += pullCommentsForUser(u)
    return HttpResponse(rv)





    # https://www.reddit.com/user/MrMediaMogul/comments/.json
    # https://www.reddit.com/user/MrMediaMogul/comments/.json?after=t1_cqjsz5e

    # TOO MANY REQUESTS ERROR format
    # {"message": "Too Many Requests", "error": 429}

    # Three queries to get user comments using after value from previous
    # https://www.reddit.com/user/stp2007/comments/.json
    # https://www.reddit.com/user/stp2007/comments/.json?after=t1_d8fi1ll
    # https://www.reddit.com/user/stp2007/comments/.json?after=t1_d6b14um

    # print ("TEST TEST TEST TEST TEST TEST TEST")

















