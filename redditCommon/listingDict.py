from helperLibrary.stringHelper import *
import json
# from django.http import HttpResponse
# from django.core.exceptions import ObjectDoesNotExist
# from .models import subreddit, subredditThreadProcessedStatus, subredditThreadIndex, subredditThreadRaw
# from redditCommon.constants import *
# from redditCommon.credentials import credentials_getAuthorizationHeader
# import requests

# *****************************************************************************
def listingDict_displayErrorMessage(d):
    rv = "<BR>ERROR MESSAGE: " + d['message']
    if 'error' in d:
        rv += ", " + "ERROR: " + str(d['error'])
    return rv

# *****************************************************************************
def listingDict_displayUnknownDict(d):
    rv = "<BR>ERROR UNKNOWN: " + json.dumps(d)
    return rv

# *****************************************************************************
def listingDict_displayMeta(d):
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
def listingDict_validate (d, argDict):
    if 'message' in d:
        argDict['rv'] += listingDict_displayErrorMessage(d)
    elif 'data' in d:
        if 'children' in d['data']:
            argDict['validateResult'] = True
            argDict['rv'] += "<BR>VALIDATES SUCCESSFULLY"
        else:
            argDict['rv'] += "<BR>ERROR: children key not found in d[data]"
    else:
        argDict['rv'] += listingDict_displayUnknownDict(d)
    return



















