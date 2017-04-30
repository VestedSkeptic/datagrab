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
    rv = "<BR>ERROR MESSAGE: " + d['message']
    if 'error' in d:
        rv += ", " + "ERROR: " + str(d['error'])
    return rv

# *****************************************************************************
def displayUnknownDict(d):
    rv = "<BR>ERROR UNKNOWN: " + json.dumps(d)
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
def validateNewCommentsDataDict (d, argDict):
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
def getDictOfNewCommentsForUser(cs, d):
    rv = "<BR>" + cs.user.name + ": AA: " + "[After: " + cs.after + "]" + " [Before: " + cs.before + "]"
    # EXAMPLE: UserName: AA: [After: processed] [Before: t1_dddddd86]

    commentQuery = buildCommentQuery(cs.user.name, cs.after, cs.before)
    rv += "<BR>commentQuery: " + commentQuery
    # EXAMPLE: commentQuery: https://oauth.reddit.com/user/OldDevLearningLinux/comments/.json?limit=100&before=t1_dejemg4

    AuthHeader = credentials_getAuthorizationHeader()
    # print ("*** %s" % (json.dumps(AuthHeader)))
    # EXAMPLE: {"User-Agent": "testscript by /u/OldDevLearningLinux", "Authorization": "bearer eAKTo07KQutnf1qCMBNphzuU9Wg"}

    r = requests.get(commentQuery, headers=AuthHeader)
    d.update(r.json())

    return rv

# *****************************************************************************
def getUsersCommentsProcessedStatus(u):
    # get userCommentsProcessedStatus for user, if not exist create on
    cs = None
    try:
        cs = userCommentsProcessedStatus.objects.get(user=u)
        print("*** userCommentsProcessedStatus already exists")
    except ObjectDoesNotExist:
        cs = userCommentsProcessedStatus(user=u)
        cs.save()
        print("*** userCommentsProcessedStatus created")
    return cs

# *****************************************************************************
def comments_updateForAllUsers():
    rv = "<B>comments_updateForAllUsers</B><BR>"
    print("=====================================================")

    users = user.objects.all()
    count = 0
    for u in users:
        count += 1
        rv += "<BR> ---------------------------------"
        print("Processing user: %s" % (u.name))
        cs = getUsersCommentsProcessedStatus(u)

        d = {}
        rv += getDictOfNewCommentsForUser(cs, d)
        print ("*** %s" % (json.dumps(d)))

        argDict = {'rv': "", 'validateResult': False}
        validateNewCommentsDataDict(d, argDict)
        rv += argDict['rv']

        if argDict['validateResult']:
            print("*** validate is true")

            rv += displayCommentListingDictMeta(d)
            # EXAMPLE: DATA: AFTER: None, BEFORE: None, MODHASH: , CHILDREN: 1

            rv += displayCommentListingDataChildren(d)
            # EXAMPLE: 1: t1_dgydfqu Reply 29b
            #          2: t1_dgydfby Reply 29a
            youngestChild = processCommentListingDataChildren(d, cs.user)

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

        rv += "<br>"
        print("")

    if count == 0:
        rv += "<BR> ---------------------------------"
        rv += "<BR> No users found"

    return HttpResponse(rv)























