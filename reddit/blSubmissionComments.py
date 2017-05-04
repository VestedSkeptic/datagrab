from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import subredditSubmissionRaw, user, userCommentsIndex, userCommentsRaw # , userCommentsProcessedStatus
from .blUserComments import blUserComments_getUserCommentIndex, blUserComments_saveUserCommentsRaw
from .constants import *
import json
import praw
import pprint

# *****************************************************************************
def blSubmissionComments_updateCommentsForSubmission(submission, argDict):
    print("Processing submission: %s: %s" % (submission.sti.name, submission.title))

    # create PRAW reddit instance
    reddit = praw.Reddit(client_id=CONST_CLIENT_ID, client_secret=CONST_SECRET, user_agent=CONST_USER_AGENT, username=CONST_DEV_USERNAME, password=CONST_DEV_PASSWORD)

    # THIS ISNT USING ANY KIND OF PROCESSED STATUS
    # get status of comments already processed by this user
    # cs = blUserComments_getUsersCommentsProcessedStatus(user)
    params={};
    # NOTE: Not using youngest currently because using it:
    #       * limits resuilts to 100 for some reason
    #       * fails if youngest doesn't exist any more (or is too old)
    # if cs.youngest != "":
    #     params['before'] = cs.youngest;

    # iterate through comments saving them
    # for comment in reddit.redditor(user.name).comments.new(limit=None, params=params):
    #     aDict = {'uci' : None, 'isNew' : True }
    #     blUserComments_getUserCommentIndex(comment, user, aDict)
    #     if aDict['isNew']:
    #         blUserComments_saveUserCommentsRaw(comment, aDict['uci'])
    #         countNew += 1
    #     else:
    #         countDuplicate += 1


    countNew = 0
    countDuplicate = 0
    countPostsWithNoAuthor = 0
    submissionObject = reddit.submission(id=submission.sti.iidd)
    submissionObject.comments.replace_more(limit=0)
    for comment in submissionObject.comments.list():
        # See if comment.author.name exists in class user(models.Model):
        # If not add it with poi value set to false.

        if comment.author == None:
            countPostsWithNoAuthor += 1
        else:
            uuser = None
            try:
                uuser = user.objects.get(name=comment.author.name)
            except ObjectDoesNotExist:
                uuser = user(name=comment.author.name, poi=False)
                uuser.save()

            aDict = {'uci' : None, 'isNew' : True }
            blUserComments_getUserCommentIndex(comment, uuser, aDict)
            if aDict['isNew']:
                blUserComments_saveUserCommentsRaw(comment, aDict['uci'])
                countNew += 1
            else:
                countDuplicate += 1

        # # print(comment.body[0:40])
        # # print(comment.author.name)
        # pprint.pprint(vars(comment))
        # break




        # # update youngest appropriately
        # if comment.name > cs.youngest:
        #     cs.youngest = comment.name

    # save cs so it contains appropriate value for youngest
    # cs.save()

    argDict['rv'] += "<br><b>" + \
        submission.sti.name + \
        ", " + \
        submission.title + \
        "</b>: " + \
        str(countNew) + \
        " new, " + \
        str(countDuplicate) + \
        " duplicated, " + \
        str(countPostsWithNoAuthor) + \
        " with no author."

    return

# *****************************************************************************
def blSubmissionComments_updateForAllSubmissions():
    print("=====================================================")
    rv = "<B>PRAW</B> blSubmissionComments_updateForAllSubmissions<BR>"

    # submission = "t3_690ved"   # https://www.reddit.com/r/politics/comments/690ved/discussion_megathread_fbi_director_comey/
    submission = "t3_699g45"   # https://www.reddit.com/r/politics/comments/699g45/megathread_republican_health_care_plan_passes/
    # submission = "t3_69a8hl"   # https://www.reddit.com/r/politics/comments/69a8hl/nancy_pelosi_on_trumpcare_this_is_a_scar_they/



    # For testing am only working on one submission_replies at a time.
    # submissions = subredditSubmissionRaw.objects.filter(sti__name=submission)
    submissions = subredditSubmissionRaw.objects.all()
    if submissions.count() == 0:
        rv += "<BR> No Submissions found"
    else:
        breakCount=50
        for sub in submissions:
            argDict = {'rv': ""}
            blSubmissionComments_updateCommentsForSubmission(sub, argDict)
            rv += argDict['rv']
            breakCount -= 1
            if breakCount == 0:
                break

    print("=====================================================")
    return HttpResponse(rv)










