from django.http import HttpResponse
from .blUserComments import blUserComments_updateForAllUsers
from .blSubredditSubmissions import blSubredditSubmissions_updateForAllSubreddits
from .blSubmissionComments import blSubmissionComments_updateForAllSubmissions
from .models import *

# *****************************************************************************
def main(request):
    s  = ''
    s += '<br><b>PRAW</b><br>'
    s += '<br><a href="http://localhost:8000/admin/reddit/">admin</a><br>'
    # s += '<br><a href="http://localhost:8000/reddit/praw/ucfau/">update user comments</a><br>'
    # s += '<br><a href="http://localhost:8000/reddit/praw/usfas/">update subreddit submissions</a><br>'
    s += '<br><a href="http://localhost:8000/reddit/praw/ucfas/">update submission comments</a><br>'
    s += displayDatabaseModelCounts()
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

    return s












