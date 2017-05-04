from django.http import HttpResponse
from .blUserComments import blUserComments_updateForAllUsers
from .blSubredditSubmissions import blSubredditSubmissions_updateForAllSubreddits
from .blSubmissionComments import blSubmissionComments_updateForAllSubmissions
# from django.shortcuts import render

# *****************************************************************************
def main(request):
    s  = ''
    s += '<br><b>PRAW</b><br>'
    s += '<br><a href="http://localhost:8000/admin/">admin</a><br>'
    s += '<br><a href="http://localhost:8000/reddit/praw/ucfau/">update user comments</a><br>'
    s += '<br><a href="http://localhost:8000/reddit/praw/usfas/">update subreddit submissions</a><br>'
    s += '<br><a href="http://localhost:8000/reddit/praw/ucfas/">update submission comments</a><br>'
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