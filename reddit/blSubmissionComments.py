from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import subredditSubmissionIndex, user, userCommentsIndex, userCommentsRaw
from .blUserComments import blUserComments_getUserCommentIndex, blUserComments_saveUserCommentsRaw
import config
from .constants import *
import json
import praw
import pprint

                    # # *****************************************************************************
                    # def blSubmissionComments_updateCommentsForSubmission(submission, argDict):
                    #     logger = getmLoggerInstance()
                    #     logger.info("Processing submission: %s: %s" % (submission.subreddit.name, submission.name))
                    #
                    #     # create PRAW prawReddit instance
                    #     prawReddit = praw.Reddit(client_id=CONST_CLIENT_ID, client_secret=CONST_SECRET, user_agent=CONST_USER_AGENT, username=CONST_DEV_USERNAME, password=CONST_DEV_PASSWORD)
                    #
                    #     # THIS ISNT USING ANY KIND OF PROCESSED STATUS
                    #     # get status of comments already processed by this user
                    #     # cs = blUserComments_getUsersCommentsProcessedStatus(user)
                    #     params={};
                    #     # NOTE: Not using youngest currently because using it:
                    #     #       * limits resuilts to 100 for some reason
                    #     #       * fails if youngest doesn't exist any more (or is too old)
                    #     # if cs.youngest != "":
                    #     #     params['before'] = cs.youngest;
                    #
                    #
                    # # TESTING
                    # # COMMENT #6: t1_dh6fz7q is youngest comment in lone MOLW submission SAVED IN DB.
                    # # COMMENT #7: t1_dh6hif7 is a newer comment in that submission.
                    # # COMMENT #8: t1_dh6hil0 is the newest comment in that thread.
                    #
                    #
                    #
                    #
                    #                                                     # Sort order and comment limit can be set with the comment_sort and comment_limit attributes before comments are fetched, including any call to replace_more():
                    #                                                     #
                    #                                                     # submission.comment_sort = 'new'
                    #                                                     # comments = submission.comments.list()
                    #
                    #
                    # # praw.helpers.comment_stream
                    # # praw.helpers.comment_stream
                    # # praw.helpers.comment_stream
                    # # praw.helpers.comment_stream
                    # # praw.helpers.comment_stream
                    #
                    #
                    #
                    #
                    # # def checkComments(comments):
                    # #   for comment in comments:
                    # #     logger.info comment.body
                    # #     checkComments(comment.replies)
                    # #
                    # # def processSub(sub):
                    # #   sub.replace_more_comments(limit=None, threshold=0)
                    # #   checkComments(sub.comments)
                    # #
                    # #
                    # # #login and subreddit init stuff here
                    # # subs = mysubreddit.get_hot(limit=50)
                    # # for sub in subs:
                    # #   processSub(sub)
                    #
                    # # GET [/r/subreddit]/newreadrss support
                    # # This endpoint is a listing
                    # #
                    # # after                       fullname of a thing
                    # # before                      fullname of a thing
                    # # count                       a positive integer (default: 0)
                    # # limit                       the maximum number of items desired (default: 25, maximum: 100)
                    # # show                        (optional) the string all
                    # # sr_detail                   (optional) expand subreddits
                    #
                    # # submission = r.get_submission(thread)
                    # # process_comments(submission.comments)
                    # #
                    # # def process_comments(objects):
                    # #     for object in objects:
                    # #         if type(object).__name__ == "Comment":
                    # #             process_comments(object.replies) # Get replies of comment
                    # #
                    # #             # Do stuff with comment (object)
                    # #
                    # #         elif type(object).__name__ == "MoreComments":
                    # #             process_comments(object.comments()) # Get more comments at same level
                    #
                    #
                    #
                    #     countNew = 0
                    #     countDuplicate = 0
                    #     countPostsWithNoAuthor = 0
                    #
                    #     # remember to wrap prawReddit calls in
                    #     # try:
                    #     #
                    #     #
                        # except praw.exceptions.APIException as e:
                        #     logger.error("PRAW APIException: error_type = %s, message = %s" % (e.error_type, e.message))
                    #
                    #     # works: gets all
                    #     submissionObject = prawReddit.submission(id=submission.name[3:])
                    #     # fails: "submission object has no attribute new"
                    #     # submissionObject = prawReddit.submission(id=submission.name[3:]).new(limit=None, params=params)
                    #
                    #
                    #     # TODO: Later review use of 0 value in limit. Should it be replaced with None?
                    #     # 0 = remove all MoreComments
                    #     # None = no limit to number of MoreComments replaced [MAX = 32]
                    #
                    #     # works: gets all
                    #     submissionObject.comments.replace_more(limit=None)
                    #     # Fails: an unexpected keyword argument 'params'
                    #     # submissionObject.comments.replace_more(limit=None, params=params)
                    #
                    #
                    #     # for comment in submissionObject.comments.list():
                    #     #     # See if comment.author.name exists in class user(models.Model):
                    #     #     # If not add it with poi value set to false.
                    #     #
                    #     #     if comment.author == None:
                    #     #         countPostsWithNoAuthor += 1
                    #     #     else:
                    #     #         uuser = None
                    #     #         try:
                    #     #             uuser = user.objects.get(name=comment.author.name)
                    #     #         except ObjectDoesNotExist:
                    #     #             uuser = user(name=comment.author.name, poi=False)
                    #     #             uuser.save()
                    #     #
                    #     #         aDict = {'uci' : None, 'isNew' : True }
                    #     #         blUserComments_getUserCommentIndex(comment, uuser, aDict)
                    #     #         if aDict['isNew']:
                    #     #             blUserComments_saveUserCommentsRaw(comment, aDict['uci'])
                    #     #             countNew += 1
                    #     #         else:
                    #     #             countDuplicate += 1
                    #
                    #         # # logger.info(comment.body[0:40])
                    #         # # logger.info(comment.author.name)
                    #         # pprint.pprint(vars(comment))
                    #         # break
                    #
                    #     argDict['rv'] += "<br><b>" + \
                    #         submission.subreddit.name + \
                    #         ", " + \
                    #         submission.name + \
                    #         "</b>: " + \
                    #         str(countNew) + \
                    #         " new, " + \
                    #         str(countDuplicate) + \
                    #         " duplicated, " + \
                    #         str(countPostsWithNoAuthor) + \
                    #         " with no author."
                    #
                    #     return

                    # # *****************************************************************************
                    # def blSubmissionComments_getMostValidBeforeValue(subreddit, prawReddit):
                    #     youngestRV = ''
                    #
                    #     for item in subredditSubmissionIndex.objects.filter(subreddit=subreddit, deleted=False).order_by('-name'):
                    #         # CAN I BATCH THIS QUERY UP TO GET MULTIPLE COMMENTS FROM REDDIT AT ONCE?
                    #         submission = prawReddit.submission(item.name[3:])
                    #         if submission.author != None:
                    #             youngestRV = item.name
                    #             break
                    #         else: # Update item as deleted.
                    #             item.deleted = True
                    #             item.save()
                    #             logger.info("subredditSubmissionIndex %s flagged as deleted" % (item.name))
                    #
                    #
                    #     return youngestRV
                    #
                    # # *****************************************************************************
                    # def blSubmissionComments_updateCommentsForSubmission_phase2_submissionIteration(subreddit, argDict):
                    #     logger.info("Processing subreddit: %s" % (subreddit.name))
                    #
                    #     # create prawReddit instance
                    #     prawReddit = praw.Reddit(client_id=CONST_CLIENT_ID, client_secret=CONST_SECRET, user_agent=CONST_USER_AGENT, username=CONST_DEV_USERNAME, password=CONST_DEV_PASSWORD)
                    #
                    #     # get youngest subredditSubmissionIndex in DB if there are any
                    #     params={};
                    #     params['before'] = blSubmissionComments_getMostValidBeforeValue(subreddit, prawReddit)
                    #     logger.info ("params[before] = %s" % params['before'])
                    #
                    #     # iterate through submissions saving them
                    #     countNew = 0
                    #     countDuplicate = 0
                    #     for submission in prawReddit.subreddit(subreddit.name).new(limit=None, params=params):
                    #         aDict = {'ssi' : None, 'isNew' : True }
                    #         blSubredditSubmissions_getsubredditSubmissionIndex(submission, subreddit, aDict)
                    #         if aDict['isNew']:
                    #             blSubredditSubmissions_savesubredditSubmissionRaw(submission, aDict['ssi'])
                    #             countNew += 1
                    #         else:
                    #             countDuplicate += 1
                    #
                    #     argDict['rv'] += "<br><b>" + subreddit.name + "</b>: " + str(countNew) + " new and " + str(countDuplicate) + " duplicate submissions processed"
                    #     return

# # *****************************************************************************
# def getCommentsByCommentForest(subIndex, argDict, sortOrder):
#     logger = getmLoggerInstance()
#     logger.debug("%s: %s: sortOrder = %s" % (subIndex.subreddit.name, subIndex.name, sortOrder))
#
#     # create PRAW prawReddit instance
#     prawReddit = praw.Reddit(client_id=CONST_CLIENT_ID, client_secret=CONST_SECRET, user_agent=CONST_USER_AGENT, username=CONST_DEV_USERNAME, password=CONST_DEV_PASSWORD)
#
#     countNew = 0
#     countDuplicate = 0
#     countPostsWithNoAuthor = 0
#     try:
#         params={};
#
#         submissionObject = prawReddit.submission(id=subIndex.name[3:])
#         submissionObject.comment_sort = sortOrder
#
#         # child 1 mule
#         # https://www.reddit.com/r/molw/comments/6afi16/thread_04/dhe47qt/
#         ccc = prawReddit.comment("dhe47qt")
#         submissionObject.comments._comments=[ccc]      # try to add a list of comments to work off of here
#         submissionObject._fetch()
#
#         submissionObject.comments.replace_more(limit=0)
#         # submissionObject.comments.replace_more(limit=None)
#         cfList = submissionObject.comments.list()
#         logger.info(pprint.pformat(cfList))
#         # for comment in submissionObject.comments.list():
#         for comment in cfList:
#
#         # # commentForest = praw.models.CommentForest(submissionObject)
#         # commentForest = praw.models.comment_forest.CommentForest(submissionObject)
#         # # submissionObject._fetch()
#         # # commentForest._fetch()
#         # commentForest.replace_more(limit=None)
#         # logger.info(pprint.pformat(vars(commentForest)))
#         # for comment in commentForest.list():
#
#
#             # See if comment.author.name exists in class user(models.Model):
#             # If not add it with poi value set to false.
#             if comment.author == None:
#                 countPostsWithNoAuthor += 1
#             else:
#                 uuser = None
#                 try:
#                     uuser = user.objects.get(name=comment.author.name)
#                     # logger.debug("user %s exists" % (uuser.name))
#                 except ObjectDoesNotExist:
#                     uuser = user(name=comment.author.name, poi=False)
#                     uuser.save()
#                     logger.trace("user %s created" % (uuser.name))
#
#                 aDict = {'uci' : None, 'isNew' : True }
#                 blUserComments_getUserCommentIndex(comment, uuser, aDict)
#                 if aDict['isNew']:
#                     blUserComments_saveUserCommentsRaw(comment, aDict['uci'])
#                     countNew += 1
#                 else:
#                     countDuplicate += 1
#     except praw.exceptions.APIException as e:
#         logger.error("PRAW APIException: error_type = %s, message = %s" % (e.error_type, e.message))
#
#     # Update subIndex appropriately
#     saveSubIndex = False
#     if sortOrder == "new":
#         subIndex.cForestGot = True
#         logger.trace("%s: %s: cForestGot set to True" % (subIndex.subreddit.name, subIndex.name))
#         saveSubIndex = True
#     if countNew > 0:
#         subIndex.count += countNew
#         logger.trace("%s: %s: count set to %d" % (subIndex.subreddit.name, subIndex.name, subIndex.count))
#         saveSubIndex = True
#     if saveSubIndex:
#         subIndex.save()
#
#     s_temp = subIndex.subreddit.name + ", " + subIndex.name + ": " + str(countNew) + " new, " + str(countDuplicate) + " duplicated, " + str(countPostsWithNoAuthor) + " with no author."
#     logger.info(s_temp)
#     argDict['rv'] += "<br>" + s_temp
#     return

# *****************************************************************************
def getCommentsByCommentForest(subIndex, argDict, sortOrder):
    clog.logger.debug("%s: %s: sortOrder = %s" % (subIndex.subreddit.name, subIndex.name, sortOrder))

    # create PRAW prawReddit instance
    prawReddit = praw.Reddit(client_id=CONST_CLIENT_ID, client_secret=CONST_SECRET, user_agent=CONST_USER_AGENT, username=CONST_DEV_USERNAME, password=CONST_DEV_PASSWORD)

    countNew = 0
    countDuplicate = 0
    countPostsWithNoAuthor = 0
    try:
        params={};

        submissionObject = prawReddit.submission(id=subIndex.name[3:])
        submissionObject.comment_sort = sortOrder
        # submissionObject.comments.replace_more(limit=0)
        # submissionObject.comments.replace_more(limit=None)
        submissionObject.comments.replace_more(limit=16)
        for comment in submissionObject.comments.list():
            # See if comment.author.name exists in class user(models.Model):
            # If not add it with poi value set to false.
            if comment.author == None:
                countPostsWithNoAuthor += 1
            else:
                uuser = None
                try:
                    uuser = user.objects.get(name=comment.author.name)
                    # clog.logger.debug("user %s exists" % (uuser.name))
                except ObjectDoesNotExist:
                    uuser = user(name=comment.author.name, poi=False)
                    uuser.save()
                    clog.logger.trace("user %s created" % (uuser.name))

                aDict = {'uci' : None, 'isNew' : True }
                blUserComments_getUserCommentIndex(comment, uuser, aDict)
                if aDict['isNew']:
                    blUserComments_saveUserCommentsRaw(comment, aDict['uci'])
                    countNew += 1
                else:
                    countDuplicate += 1
    except praw.exceptions.APIException as e:
        clog.logger.error("PRAW APIException: error_type = %s, message = %s" % (e.error_type, e.message))

    # Update subIndex appropriately
    saveSubIndex = False
    if sortOrder == "new":
        subIndex.cForestGot = True
        clog.logger.trace("%s: %s: cForestGot set to True" % (subIndex.subreddit.name, subIndex.name))
        saveSubIndex = True
    if countNew > 0:
        subIndex.count += countNew
        clog.logger.trace("%s: %s: count set to %d" % (subIndex.subreddit.name, subIndex.name, subIndex.count))
        saveSubIndex = True
    if saveSubIndex:
        subIndex.save()

    s_temp = subIndex.subreddit.name + ", " + subIndex.name + ": " + str(countNew) + " new, " + str(countDuplicate) + " duplicated, " + str(countPostsWithNoAuthor) + " with no author."
    clog.logger.info(s_temp)
    argDict['rv'] += "<br>" + s_temp
    return

# *****************************************************************************
def updateSubIndexComments(subIndex, argDict):
    if not subIndex.cForestGot:
        clog.logger.trace("%s: %s: New commentForest updating sorted by new" % (subIndex.subreddit.name, subIndex.name))
        getCommentsByCommentForest(subIndex, argDict, "new")
        argDict['modeCount']['Comment Forest New'] += 1
    # elif subIndex.count < 10:
    #     clog.logger.debug("%s: %s: Old small commentForest updating sorted by old" % (subIndex.subreddit.name, subIndex.name))
    #     getCommentsByCommentForest(subIndex, argDict, "old")
        # argDict['modeCount']['Comment Forest Old'] += 1
                    # THIS HACK NOT VALID, SUBMISSION UPDATED AND HAS NEW COUNT NOW
                    # elif subIndex.count == 260:  #HACK THERE IS ONE ITEM WITH 260 COUNT IN IT, USING IT TO TEST IMPLEMENTATION OF ...
                    #     clog.logger.debug("%s: %s: Old small commentForest updating sorted by old" % (subIndex.subreddit.name, subIndex.name))
                    #     getCommentsByCommentForest(subIndex, argDict, "old")
                    #     argDict['modeCount']['Comment Forest Old'] += 1
    else:
        clog.logger.trace("%s: %s: Old large commentForest updating by METHOD TO BE IMPLEMENTED LATER" % (subIndex.subreddit.name, subIndex.name))
        argDict['modeCount']['Method To Be Implemented Later'] += 1

# *****************************************************************************
def blSubmissionComments_updateForAllSubmissions():
    clog.logger.info("=====================================================")
    clog.logger.info("blSubmissionComments_updateForAllSubmissions()")
    rv = "<B>PRAW</B> blSubmissionComments_updateForAllSubmissions<BR>"

    submissionsIndexObjects =subredditSubmissionIndex.objects.filter(deleted=False).order_by('subreddit__name')
    if submissionsIndexObjects.count() == 0:
        rv += "<BR> No Submissions found"
    else:
        argDict = {'rv': "", 'modeCount': {'Comment Forest New' : 0, 'Comment Forest Old' : 0, 'Method To Be Implemented Later' : 0, }}
        for subIndex in submissionsIndexObjects:
            updateSubIndexComments(subIndex, argDict)
        rv += argDict['rv']

        s_temp = "Comment Forest New count" + " = " + str(argDict['modeCount']['Comment Forest New'])
        clog.logger.info(s_temp)
        rv += "<br>" + s_temp
        s_temp = "Comment Forest Old count" + " = " + str(argDict['modeCount']['Comment Forest Old'])
        clog.logger.info(s_temp)
        rv += "<br>" + s_temp
        s_temp = "Method To Be Implemented Later count" + " = " + str(argDict['modeCount']['Method To Be Implemented Later'])
        clog.logger.info(s_temp)
        rv += "<br>" + s_temp

    clog.logger.info("=====================================================")
    return HttpResponse(rv)










