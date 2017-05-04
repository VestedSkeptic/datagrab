from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import user, userCommentsProcessedStatus, userCommentsIndex, userCommentsRaw
from .constants import *
import json
import praw
# import pprint

# *****************************************************************************
# get userCommentsProcessedStatus for user, if not exist create on
def blUserComments_getUsersCommentsProcessedStatus(user):
    cs = None
    try:
        cs = userCommentsProcessedStatus.objects.get(user=user)
    except ObjectDoesNotExist:
        cs = userCommentsProcessedStatus(user=user)
        cs.save()
    return cs

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

    # get status of comments already processed by this user
    cs = blUserComments_getUsersCommentsProcessedStatus(user)
    params={};
    # NOTE: Not using youngest currently because using it:
    #       * limits resuilts to 100 for some reason
    #       * fails if youngest doesn't exist any more (or is too old)
    # if cs.youngest != "":
    #     params['before'] = cs.youngest;

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

        # update youngest appropriately
        if comment.name > cs.youngest:
            cs.youngest = comment.name

    # save cs so it contains appropriate value for youngest
    cs.save()

    argDict['rv'] += "<br><b>" + user.name + "</b>: " + str(countNew) + " new and " + str(countDuplicate) + " duplicate comments processed"

    return

# *****************************************************************************
def blSubmissionComments_updateForAllSubmissions():
    print("=====================================================")
    rv = "<B>PRAW</B> blSubmissionComments_updateForAllSubmissions<BR>"

    submission = "690ved"   # https://www.reddit.com/r/politics/comments/690ved/discussion_megathread_fbi_director_comey/
    submission = "699g45"   # https://www.reddit.com/r/politics/comments/699g45/megathread_republican_health_care_plan_passes/
    submission = "69a8hl"   # https://www.reddit.com/r/politics/comments/69a8hl/nancy_pelosi_on_trumpcare_this_is_a_scar_they/


    # For testing am only working on one submission_replies at a time.

    # users = user.objects.filter(poi=True)
    # if users.count() == 0:
    #     rv += "<BR> No users found"
    # else:
    #     for us in users:
    #         argDict = {'rv': ""}
    #         blUserComments_updateCommentsForUser(us, argDict)
    #         rv += argDict['rv']
    print("=====================================================")
    return HttpResponse(rv)










