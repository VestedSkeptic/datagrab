from django.http import HttpResponse
from .blUserComments import blUserComments_updateForAllUsers
from .blSubredditSubmissions import blSubredditSubmissions_updateForAllSubreddits
from .blSubmissionComments import blSubmissionComments_updateForAllSubmissions
from .models import *
# from django.shortcuts import render

# *****************************************************************************
def main(request):
    s  = ''
    s += '<br><b>PRAW</b><br>'
    s += '<br><a href="http://localhost:8000/admin/">admin</a><br>'
    s += '<br><a href="http://localhost:8000/reddit/praw/ucfau/">update user comments</a><br>'
    s += '<br><a href="http://localhost:8000/reddit/praw/usfas/">update subreddit submissions</a><br>'
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
    users_poi           = user.objects.filter(poi=True).count()
    users_notPoi        = user.objects.filter(poi=False).count()
    users_cps           = userCommentsProcessedStatus.objects.all().count()
    users_ci            = userCommentsIndex.objects.all().count()

    subreddits          = subreddit.objects.all().count()
    subreddits_sps      = subredditSubmissionIndex.objects.all().count()
    subreddits_si       = subredditSubmissionIndex.objects.all().count()

    s = ''
    s += '<BR>==========================='
    s += '<BR>Users POI = ' + str(users_poi)
    s += '<BR>Users not POI = ' + str(users_notPoi)
    s += '<BR>Total Users = ' + str(users_poi + users_notPoi)
    if users_cps == users_ci:
        s += '<BR>Users comments saved = ' + str(users_cps)
    else:
        s += '<BR>WARNING: Dicrepency in Users comments saved'
        s += '<BR>users_cps = ' + str(users_cps)
        s += '<BR>users_ci = ' + str(users_ci)
    s += '<BR>'
    s += '<BR>Subreddits = ' + str(subreddits)
    if subreddits_sps == subreddits_si:
        s += '<BR>Subreddit comments saved = ' + str(subreddits_sps)
    else:
        s += '<BR>WARNING: Dicrepency in Subreddit comments saved'
        s += '<BR>subreddits_sps = ' + str(subreddits_sps)
        s += '<BR>subreddits_si = ' + str(subreddits_si)
    s += '<BR>==========================='

    return s