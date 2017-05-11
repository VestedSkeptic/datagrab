from django.http import HttpResponse
from .blUserComments import blUserComments_updateForAllUsers, getHierarchyOfCommentsAtLevel
from .blSubredditSubmissions import blSubredditSubmissions_updateForAllSubreddits
from .blSubmissionComments import blSubmissionComments_updateForAllSubmissions
from .models import *

# *****************************************************************************
def main(request):
    s  = ''
    s += '<br><b>PRAW</b><br>'
    s += '<br><a href="http://localhost:8000/admin/reddit/">admin</a><br>'
    s += '<br><a href="http://localhost:8000/reddit/praw/ucfau/">update user comments</a><br>'
    s += '<br><a href="http://localhost:8000/reddit/praw/usfas/">update subreddit submissions</a><br>'
    s += '<br><a href="http://localhost:8000/reddit/praw/ucfas/">update submission comments</a><br>'

    s += '<br><b>ParseCommentHeirarchy: </b>'
    s += '<a href="http://localhost:8000/reddit/praw/pch/0">0</a>, '
    s += '<a href="http://localhost:8000/reddit/praw/pch/1">1</a>, '
    s += '<a href="http://localhost:8000/reddit/praw/pch/2">2</a>, '
    s += '<a href="http://localhost:8000/reddit/praw/pch/3">3</a>, '
    s += '<a href="http://localhost:8000/reddit/praw/pch/4">4</a>, '
    s += '<a href="http://localhost:8000/reddit/praw/pch/5">5</a>, '
    s += '<a href="http://localhost:8000/reddit/praw/pch/6">6</a>, '
    s += '<a href="http://localhost:8000/reddit/praw/pch/7">7</a>, '
    s += '<a href="http://localhost:8000/reddit/praw/pch/8">8</a>, '
    s += '<a href="http://localhost:8000/reddit/praw/pch/9">9</a>, '
    s += '<a href="http://localhost:8000/reddit/praw/pch/10">10</a>, '
    s += '<a href="http://localhost:8000/reddit/praw/pch/11">11</a>, '
    s += '<a href="http://localhost:8000/reddit/praw/pch/12">12</a>, '

    s += '<br>' + displayDatabaseModelCounts()
    s += '<br><a href="http://localhost:8000/reddit/praw/dau/">delete all users</a><br>'
    s += '<br><a href="http://localhost:8000/reddit/praw/das/">delete all subreddits</a><br>'
    return HttpResponse(s)

# *****************************************************************************
def updateCommentsForAllUsers(request):
    s = blUserComments_updateForAllUsers()
    return HttpResponse(s)

# *****************************************************************************
def updateSubmissionsForAllSubreddits(request):
    s = blSubredditSubmissions_updateForAllSubreddits()
    return HttpResponse(s)

# *****************************************************************************
def updateCommentsForAllSubmissions(request):
    s = blSubmissionComments_updateForAllSubmissions()
    return HttpResponse(s)

# *****************************************************************************
def updateSubmissionsForAllSubreddits(request):
    s = blSubredditSubmissions_updateForAllSubreddits()
    return HttpResponse(s)

# *****************************************************************************
def displayDatabaseModelCounts():
    users_poi               = user.objects.filter(poi=True).count()
    users_notPoi            = user.objects.filter(poi=False).count()

    users_ci                = userCommentsIndex.objects.filter(deleted=False).count()
    users_ci_deleted        = userCommentsIndex.objects.filter(deleted=True).count()

    subreddits              = subreddit.objects.all().count()

    subreddits_si           = subredditSubmissionIndex.objects.filter(deleted=False).count()
    subreddits_si_deleted   = subredditSubmissionIndex.objects.filter(deleted=True).count()

    s = ''
    s += '<BR>==========================='
    s += '<BR>Users POI = ' + str(users_poi)
    s += '<BR>Users not POI = ' + str(users_notPoi)
    s += '<BR>'
    s += '<BR>Users Comments = ' + str(users_ci)
    s += '<BR>Users Comments Deleted = ' + str(users_ci_deleted)
    s += '<BR>'
    s += '<BR>Subreddits = ' + str(subreddits)
    s += '<BR>'
    s += '<BR>Subreddit Submissions = ' + str(subreddits_si)
    s += '<BR>Subreddit Submissions Deleted = ' + str(subreddits_si_deleted)
    s += '<BR>==========================='
    s += '<BR>'
    return s

# *****************************************************************************
def deleteAllUsers(request):
    # get all user objects and its count
    uqs = user.objects.all()
    uqsCount = uqs.count()

    # delete all user objects
    uqs.delete()

    s = str(uqsCount) + " users deleted"
    return HttpResponse(s)

# *****************************************************************************
def deleteAllSubreddits(request):
    # get all subreddit objects and its count
    sqs = subreddit.objects.all()
    sqsCount = sqs.count()

    # delete all subreddit objects
    sqs.delete()

    s = str(sqsCount) + " subreddit deleted"
    return HttpResponse(s)

# *****************************************************************************
def parseCommentHeirarchy(request, hLevel):

    # for testing purposes get submissionIndex with MOST number of comments
    sIndex = subredditSubmissionIndex.objects.filter(cForestGot=True).order_by('-count')

    for item in sIndex:
        s = getHierarchyOfCommentsAtLevel(item.name, int(hLevel))
        break # as we are only doing one item for now

    return HttpResponse(s)









