from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import user, commentStatus
from .defines import *
from helperLibrary.stringHelper import *
import requests
import requests.auth
import json

# ref: https://github.com/reddit/reddit/wiki/OAuth2-Quick-Start-Example

# *****************************************************************************
CONST_CLIENT_ID     = "kcksu9E4VgC0TQ"
CONST_SECRET        = "Megl7I6XKHtGIQ0T4_q62KiaRQw"
CONST_GRANT_TYPE    = "client_credentials"
CONST_DEV_USERNAME  = "OldDevLearningLinux"
CONST_DEV_PASSWORD  = "ygHOwxJELMzcwZP4Wi4pO72B"
CONST_USER_AGENT    = "testscript by OldDevLearningLinux"

# *****************************************************************************
def credentials_get():
    rv = "<BR>credentials_get"

    # get token
    client_auth = requests.auth.HTTPBasicAuth(CONST_CLIENT_ID, CONST_SECRET)
    post_data = {"grant_type": CONST_GRANT_TYPE, "username": CONST_DEV_USERNAME, "password": CONST_DEV_PASSWORD}
    headers = {"User-Agent": CONST_USER_AGENT}
    response = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=client_auth,
        data=post_data,
        headers=headers)
    # ex: {"access_token": "5Aj6ERpE4I3-RalhKagFdSgxpb8", "expires_in": 3600, "scope": "*", "token_type": "bearer"}
    d = response.json()
    rv += '<BR>' + json.dumps(d)

    # use token
    # headers = {"Authorization": "bearer fhTdafZI-0ClEzzYORfBSCR7x3M", "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    auth_token = "bearer " + d['access_token']
    # auth_token = d['access_token']
    headers = {"Authorization": auth_token, "User-Agent": CONST_USER_AGENT}
    rv += '<BR>' + json.dumps(headers)
    # response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    response = requests.get("https://oauth.reddit.com/user/stp2007/comments/.json", headers=headers)


# https://www.reddit.com/user/stp2007/comments/.json


    print (response)
    d = response.json()
    rv += '<BR>' + json.dumps(d)

    return HttpResponse(rv)





