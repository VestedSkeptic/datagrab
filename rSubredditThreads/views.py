from django.http import HttpResponse
from .threads import threads_updateForAllSubreddits

# *****************************************************************************
def updateSubredditThreads(request):
    s = threads_updateForAllSubreddits()
    return HttpResponse(s)













