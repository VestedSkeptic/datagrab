from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
# from .models import subredditSubmissionRaw, user, userCommentsIndex, userCommentsRaw
from .models import subredditSubmissionIndex, user, userCommentsIndex, userCommentsRaw
from .blUserComments import blUserComments_getUserCommentIndex, blUserComments_saveUserCommentsRaw
from .constants import *
import json
import praw
import pprint

# *****************************************************************************
def blSubmissionComments_updateCommentsForSubmission(submission, argDict):
    print("Processing submission: %s: %s" % (submission.subreddit.name, submission.name))

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


# TESTING
# COMMENT #6: t1_dh6fz7q is youngest comment in lone MOLW submission SAVED IN DB.
# COMMENT #7: t1_dh6hif7 is a newer comment in that submission.
# COMMENT #8: t1_dh6hil0 is the newest comment in that thread.


    countNew = 0
    countDuplicate = 0
    countPostsWithNoAuthor = 0

    # works: gets all
    submissionObject = reddit.submission(id=submission.name[3:])
    # fails: "submission object has no attribute new"
    # submissionObject = reddit.submission(id=submission.name[3:]).new(limit=None, params=params)


    # TODO: Later review use of 0 value in limit. Should it be replaced with None?
    # 0 = remove all MoreComments
    # None = no limit to number of MoreComments replaced [MAX = 32]

    # works: gets all
    submissionObject.comments.replace_more(limit=None)
    # Fails: an unexpected keyword argument 'params'
    # submissionObject.comments.replace_more(limit=None, params=params)


    # for comment in submissionObject.comments.list():
    #     # See if comment.author.name exists in class user(models.Model):
    #     # If not add it with poi value set to false.
    #
    #     if comment.author == None:
    #         countPostsWithNoAuthor += 1
    #     else:
    #         uuser = None
    #         try:
    #             uuser = user.objects.get(name=comment.author.name)
    #         except ObjectDoesNotExist:
    #             uuser = user(name=comment.author.name, poi=False)
    #             uuser.save()
    #
    #         aDict = {'uci' : None, 'isNew' : True }
    #         blUserComments_getUserCommentIndex(comment, uuser, aDict)
    #         if aDict['isNew']:
    #             blUserComments_saveUserCommentsRaw(comment, aDict['uci'])
    #             countNew += 1
    #         else:
    #             countDuplicate += 1

        # # print(comment.body[0:40])
        # # print(comment.author.name)
        # pprint.pprint(vars(comment))
        # break

    argDict['rv'] += "<br><b>" + \
        submission.subreddit.name + \
        ", " + \
        submission.name + \
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

    submissions =subredditSubmissionIndex.objects.filter(deleted=False).order_by('subreddit__name')
    if submissions.count() == 0:
        rv += "<BR> No Submissions found"
    else:
        for sub in submissions:
            argDict = {'rv': ""}
            blSubmissionComments_updateCommentsForSubmission(sub, argDict)
            rv += argDict['rv']

    print("=====================================================")
    return HttpResponse(rv)










