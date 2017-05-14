from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from ..config import clog
from ..models import mthread

# *****************************************************************************
def list(request):
    clog.dumpMethodInfo()
    qs = mthread.objects.all()
    vs = "<br>mthread.list: "

    if qs.count() == 0:
        vs += "No items to list"

    for item in qs:
        vs += item.name + ", "

    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)

# *****************************************************************************
def delAll(request):
    clog.dumpMethodInfo()
    vs = "<br>mthread.delAll: "

    qs = mthread.objects.all()
    vs += str(qs.count()) + " mSubmissions deleted"
    qs.delete()

    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)


















#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#     s += '<br><a href="http://localhost:8000/reddit/praw/usfas/">update subreddit submissions</a>'
#
# # *****************************************************************************
# def updateSubmissionsForAllSubreddits(request):
#     s = blSubredditSubmissions_updateForAllSubreddits()
#     return HttpResponse(s)
#
#
#
#


