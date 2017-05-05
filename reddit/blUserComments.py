from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import user, userCommentsIndex, userCommentsRaw
from .constants import *
import json
import praw
# import pprint

# *****************************************************************************
# if userCommentsIndex exists return it otherwise create it
def blUserComments_getUserCommentIndex(comment, user, aDict):
    uci = None
    try:
        uci = userCommentsIndex.objects.get(user=user, name=comment.name)
        aDict['isNew'] = False
    except ObjectDoesNotExist:
        uci = userCommentsIndex(user=user, name=comment.name)
        uci.save()
    aDict['uci'] = uci
    return


# *****************************************************************************
# if blUserComments_saveUserCommentsRaw does not exist save it.
# TODO else compare appropriate fields, if any differences record appropriately
def blUserComments_saveUserCommentsRaw(comment, uci):
    ucr = None
    try:
        ucr = userCommentsRaw.objects.get(uci=uci)
    except ObjectDoesNotExist:
        # vars converts comment to json dict which can be saved to DB
        ucr = userCommentsRaw(uci=uci, data=vars(comment))
        ucr.save()
    return

# *****************************************************************************
def blUserComments_updateCommentsForUser(user, argDict):
    print("Processing user: %s" % (user.name))

    # create PRAW reddit instance
    reddit = praw.Reddit(client_id=CONST_CLIENT_ID, client_secret=CONST_SECRET, user_agent=CONST_USER_AGENT, username=CONST_DEV_USERNAME, password=CONST_DEV_PASSWORD)

    # get youngest userCommentsIndex in DB if there are any
    params={};
    params['before'] = ''
    qs = userCommentsIndex.objects.filter(user=user).order_by('-name')
    if qs.count() > 0:
        params['before'] = qs[0].name
    print ("params[before] = %s" % params['before'])

    # iterate through comments saving them
    countNew = 0
    countDuplicate = 0
    for comment in reddit.redditor(user.name).comments.new(limit=None, params=params):
        aDict = {'uci' : None, 'isNew' : True }
        blUserComments_getUserCommentIndex(comment, user, aDict)
        if aDict['isNew']:
            blUserComments_saveUserCommentsRaw(comment, aDict['uci'])
            countNew += 1
        else:
            countDuplicate += 1

    argDict['rv'] += "<br><b>" + user.name + "</b>: " + str(countNew) + " new and " + str(countDuplicate) + " duplicate comments processed"
    return

# *****************************************************************************
def blUserComments_updateForAllUsers():
    print("=====================================================")
    rv = "<B>PRAW</B> blUserComments_updateForAllUsers<BR>"

    users = user.objects.filter(poi=True)
    if users.count() == 0:
        rv += "<BR> No users found"
    else:
        for us in users:
            argDict = {'rv': ""}
            blUserComments_updateCommentsForUser(us, argDict)
            rv += argDict['rv']
    print("=====================================================")
    return HttpResponse(rv)












