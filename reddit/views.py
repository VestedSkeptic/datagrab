from django.http import HttpResponse
from .comments import comments_updateForAllUsers
from .threads import threads_updateForAllSubreddits
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
    s = comments_updateForAllUsers()
    return HttpResponse(s)

# *****************************************************************************
def updateThreadsForAllSubreddits(request):
    s = threads_updateForAllSubreddits()
    return HttpResponse(s)