from django.http import HttpResponse
from redditusers.models import reddituser
import requests, json
from helperLibrary.stringHelper import *

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
def getCommentQuery(redditusername, after):
    rv = 'https://www.reddit.com/user/'
    rv += redditusername
    rv += '/comments/.json'
    if after is not None:
        rv += '?after='
        rv += after
    return rv

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
def processRedditUsersComments(redditusername, after):
    rv = ""

    commentQuery = getCommentQuery(redditusername, after)
    rv += commentQuery
    rv += "<br> [AA: after = " + stringHelper_returnStringValueOrNone(after) + "]<BR>"

    r = requests.get(commentQuery)
    d = r.json()

    if 'message' in d:
        rv += displayMessageFromDict(d)
    elif 'data' in d:
        rv += displayCommentListingDictMeta(d)
        rv += processCommentListingDataChildren(d)

        # rv += "<br> [B1: after = " + stringHelper_returnStringValueOrNone(d['data']['after']) + "]<BR>"
        # if d['data']['after'] is not None:
        rv += "<br> [DD: after = " + stringHelper_returnStringValueOrNone(d['data']['after']) + "]<BR>"
        u = reddituser.objects.get(username=redditusername)
        u.commentsafter = d['data']['after']
        u.save()
    else:
        rv += displayUnknownDict(d)
    return rv

# *****************************************************************************
def index(request):
    all_entries = reddituser.objects.all()

    print ("TEST TEST TEST TEST TEST TEST TEST")

    rv = ""
    for entry in all_entries:
        rv += processRedditUsersComments(entry.username, entry.commentsafter)
    return HttpResponse(rv)




# https://www.reddit.com/user/MrMediaMogul/comments/.json
# https://www.reddit.com/user/MrMediaMogul/comments/.json?after=t1_cqjsz5e

















# TOO MANY REQUESTS ERROR format
# {"message": "Too Many Requests", "error": 429}


# Three queries to get user comments using after value from previous
# https://www.reddit.com/user/stp2007/comments/.json
# https://www.reddit.com/user/stp2007/comments/.json?after=t1_d8fi1ll
# https://www.reddit.com/user/stp2007/comments/.json?after=t1_d6b14um




























