from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import user, commentStatus
from .defines import *
from helperLibrary.stringHelper import *
import requests, json


# def index(request):
#     r = requests.get('https://www.reddit.com/user/BeneficEvil/comments/.json')
#     d = r.json()
#     # return HttpResponse(d.keys())     # works
#     # return HttpResponse(d['kind'])    # works
#     # return HttpResponse(d['data']['modhash'])     #fails
#     # return HttpResponse(r, content_type="application/json") # works
#     # return HttpResponse(d['data']['children'][0]['kind'])     # works
#     # return HttpResponse(d['data']['children'][0]['data']['link_id']) #works
#     return HttpResponse(d['data']['children'][0]['data']['body']) #works



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
    rv = "KIND: "
    if 'kind' in d: rv += d['kind']
    else:           rv += "ERROR kind NOT FOUND"

    if 'data' in d:
        rv += ", DATA: "
        if 'after' in d['data']:    rv += "AFTER: "       + stringHelper_returnStringValueOrNone(d['data']['after'])   + ", "
        if 'before' in d['data']:   rv += "BEFORE: "      + stringHelper_returnStringValueOrNone(d['data']['before'])  + ", "
        if 'modhash' in d['data']:  rv += "MODHASH: "     + stringHelper_returnStringValueOrNone(d['data']['modhash']) + ", "
        if 'children' in d['data']: rv += "CHILDREN: "    + str(len(d['data']['children']))
    else:
        rv += "ERROR data NOT FOUND"
    return rv

# *****************************************************************************
# def processCommentListingDataChildren(d, after):
def processCommentListingDataChildren(d):
    rv = "<br>"
    if 'children' in d['data']:
        count = 0
        for cd in d['data']['children']:
            count += 1
            rv += "<BR><b>" + str(count) + " " + cd['data']['name'] + "</b> " + cd['data']['body'] + "<br>"
    return rv;

# *****************************************************************************
def buildCommentQuery(name, after, before):
    rv = 'https://www.reddit.com/user/'
    rv += name
    rv += '/comments/.json'

    if after == CONST_UNPROCESSED:
        pass
    elif after != CONST_PROCESSED:
        rv += '?after=' + after
    else:
        if before == CONST_UNPROCESSED:
            pass
        elif before != CONST_PROCESSED:
            rv += '?before=' + before
        else:
            pass

    return rv

# *****************************************************************************
# def requestCommentsForUser(redditusername, after):
def requestCommentsForUser(cs):
    rv = "<BR>requestCommentsForUser"

    commentQuery = buildCommentQuery(cs.user.name, cs.after, cs.before)
    rv += "<BR>commentQuery: " + commentQuery

    r = requests.get(commentQuery)
    d = r.json()

    if 'message' in d:
        rv += displayMessageFromDict(d)
    elif 'data' in d:
        rv += displayCommentListingDictMeta(d)
        rv += processCommentListingDataChildren(d)

        if d['data']['after'] is not None:
            cs.after = d['data']['after']
        else:
            cs.after = CONST_PROCESSED
            cs.before = d['data']['children'][0]['data']['name']
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
    rv = "<BR>pullCommentsForUser: AA: " + "[After: " + cs.after + "]" + " [Before: " + cs.before + "]"
    rv += requestCommentsForUser(cs)
    rv += "<BR>pullCommentsForUser: BB: " + "[After: " + cs.after + "]" + " [Before: " + cs.before + "]"

    return rv

# *****************************************************************************
def comments_updateForAllUsers():
    rv = "<BR>comments_updateForAllUsers"
    users = user.objects.all()
    for u in users:
        rv += "<BR>" + u.name
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

















