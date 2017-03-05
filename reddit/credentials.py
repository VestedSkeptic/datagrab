from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import user, userCommentsProcessedStatus
from .defines import *
from helperLibrary.stringHelper import *
import requests
import requests.auth
import json
import time

# ref: https://github.com/reddit/reddit/wiki/OAuth2-Quick-Start-Example

# *****************************************************************************
CONST_CLIENT_ID         = "kcksu9E4VgC0TQ"
CONST_SECRET            = "Megl7I6XKHtGIQ0T4_q62KiaRQw"
CONST_GRANT_TYPE        = "client_credentials"
CONST_DEV_USERNAME      = "OldDevLearningLinux"
CONST_DEV_PASSWORD      = "ygHOwxJELMzcwZP4Wi4pO72B"
CONST_USER_AGENT        = "testscript by /u/OldDevLearningLinux"

# *****************************************************************************
GLOBAL_LastTokenTime    = 0
GLOBAL_AuthHeader       = {'Authorization': "", 'User-Agent': CONST_USER_AGENT}

# *****************************************************************************
def getTokenAsDict():
    client_auth = requests.auth.HTTPBasicAuth(CONST_CLIENT_ID, CONST_SECRET)
    post_data = {"grant_type": CONST_GRANT_TYPE, "username": CONST_DEV_USERNAME, "password": CONST_DEV_PASSWORD}
    headers = {"User-Agent": CONST_USER_AGENT}
    response = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=client_auth,
        data=post_data,
        headers=headers)
    d = response.json()

    # ex: {"access_token": "5Aj6ERpE4I3-RalhKagFdSgxpb8", "expires_in": 3600, "scope": "*", "token_type": "bearer"}
    return d

# *****************************************************************************
def buildAuthHeader(d):
    # headers = {"Authorization": "bearer fhTdafZI-0ClEzzYORfBSCR7x3M", "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    auth_token = "bearer " + d['access_token']
    # auth_token = d['access_token']

    global GLOBAL_AuthHeader
    GLOBAL_AuthHeader['Authorization'] = auth_token

# *****************************************************************************
def credentials_getAuthorizationHeader():
    ticks = time.time()
    if (ticks - GLOBAL_LastTokenTime) > 3500:
        print ("Last token expired, getting new one")
        d = getTokenAsDict()
        buildAuthHeader(d)
        global GLOBAL_LastTokenTime
        GLOBAL_LastTokenTime = ticks
    else:
        s = "Last token still valid, returning existing one which is good for another "
        s += str(int(3500 - (ticks - GLOBAL_LastTokenTime)))
        s += " seconds"
        print (s)
    return GLOBAL_AuthHeader






