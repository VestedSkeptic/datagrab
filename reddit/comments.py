from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import user, userCommentsProcessedStatus, userCommentsIndex, userCommentsRaw
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
def processCommentListingDataChildren(d, u):
    youngestChild = ""
    if 'children' in d['data']:
        for cd in d['data']['children']:
            if cd['data']['name'] > youngestChild:
                youngestChild = cd['data']['name']

            # see if userCommentsIndex exists, create if necessary
            uc = None
            try:
                uc = userCommentsIndex.objects.get(user=u, name=cd['data']['name'])
                s = "WARNING: userCommentsIndex: " + uc.name + " already exists"
                print(s)
            except ObjectDoesNotExist:
                uc = userCommentsIndex(user=u, name=cd['data']['name'])
                uc.save()
                s = "userCommentsIndex: " + uc.name + " created"
                print(s)

            # see if userCommentsRaw exists, create if necessary
            ucr = None
            try:
                ucr = userCommentsRaw.objects.get(uci=uc)
                s = "WARNING: userCommentsRaw: " + ucr.uci.name + " for user " + ucr.uci.user.name + " already exists"
                print(s)
            except ObjectDoesNotExist:
                ucr = userCommentsRaw(uci=uc, data=cd['data'])
                ucr.save()
                s = "userCommentsRaw: " + ucr.uci.name + " already exists"
                print(s)
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
        youngestChild = processCommentListingDataChildren(d, cs.user)
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
    # get userCommentsProcessedStatus for user, if not exist create one
    cs = None
    try:
        cs = userCommentsProcessedStatus.objects.get(user=u)
    except ObjectDoesNotExist:
        cs = userCommentsProcessedStatus(user=u)
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
        rv += "<BR> ---------------------------------"
        rv += "<BR>" + u.name + ":"
        rv += pullCommentsForUser(u)
        rv += "<br>"
    return HttpResponse(rv)























