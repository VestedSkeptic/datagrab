from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import user, userCommentsProcessedStatus, userCommentsIndex, userCommentsRaw
from .constants import *
import json
import praw
# import pprint

# *****************************************************************************
# get userCommentsProcessedStatus for user, if not exist create on
def getUsersCommentsProcessedStatus(user):
    cs = None
    try:
        cs = userCommentsProcessedStatus.objects.get(user=user)
    except ObjectDoesNotExist:
        cs = userCommentsProcessedStatus(user=user)
        cs.save()
    return cs

# *****************************************************************************
# if userCommentsIndex exists return it otherwise create it
def getUserCommentIndex(comment, user):
    uci = None
    try:
        uci = userCommentsIndex.objects.get(user=user, name=comment.name)
        print ("WARNING: getUserCommentIndex: " + uci.name + " already exists");
    except ObjectDoesNotExist:
        uci = userCommentsIndex(user=user, name=comment.name)
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
def updateCommentsForUser(user, argDict):
    print("Processing user: %s" % (user.name))

    # create PRAW reddit instance
    reddit = praw.Reddit(client_id=CONST_CLIENT_ID, client_secret=CONST_SECRET, user_agent=CONST_USER_AGENT, username=CONST_DEV_USERNAME, password=CONST_DEV_PASSWORD)

    # get status of comments already processed by this user
    cs = getUsersCommentsProcessedStatus(user)
    params={};
    if cs.youngest != "":
        params['before'] = cs.youngest;

    # iterate through comments saving them
    count = 0
    for comment in reddit.redditor(user.name).comments.new(limit=None, params=params):
        uci = getUserCommentIndex(comment, user)
        saveUserCommentsRaw(comment, uci)
        # update youngest appropriately
        if comment.name > cs.youngest:
            cs.youngest = comment.name
        count += 1

    # save cs so it contains appropriate value for youngest
    cs.save()

    argDict['rv'] += "<br><b>" + user.name + "</b>: " + str(count) + " comments processed."
    return

# *****************************************************************************
def comments_updateForAllUsers():
    print("=====================================================")
    rv = "<B>PRAW</B> comments_updateForAllUsers<BR>"

    users = user.objects.filter(poi=True)
    if users.count() == 0:
        rv += "<BR> No users found"
    else:
        for us in users:
            argDict = {'rv': ""}
            updateCommentsForUser(us, argDict)
            rv += argDict['rv']
    print("=====================================================")
    return HttpResponse(rv)




















