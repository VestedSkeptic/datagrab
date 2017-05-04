from django.http import HttpResponse
from .blUserComments import blUserComments_updateForAllUsers
from .blSubredditSubmissions import blSubredditSubmissions_updateForAllSubreddits
# from django.shortcuts import render

# *****************************************************************************
def main(request):
    s  = ''
    s += '<br><b>PRAW</b><br>'
    s += '<br><a href="http://localhost:8000/admin/">admin</a><br>'
    s += '<br><a href="http://localhost:8000/reddit/praw/uc/">update user comments</a><br>'
    s += '<br><a href="http://localhost:8000/reddit/praw/ut/">update subreddit threads</a><br>'
    return HttpResponse(s)

# *****************************************************************************
def updateCommentsForAllUsers(request):
    s = blUserComments_updateForAllUsers()
    return HttpResponse(s)

# *****************************************************************************
def updateThreadsForAllSubreddits(request):
    s = blSubredditSubmissions_updateForAllSubreddits()
    return HttpResponse(s)