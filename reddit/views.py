from django.http import HttpResponse
from .comments import comments_updateForAllUsers
from .threads import threads_updateForAllSubreddits
# from django.shortcuts import render

# *****************************************************************************
def updateCommentsForAllUsers(request):
    s = comments_updateForAllUsers()
    return HttpResponse(s)

# *****************************************************************************
def updateThreadsForAllSubreddits(request):
    s = threads_updateForAllSubreddits()
    return HttpResponse(s)