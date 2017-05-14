from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
import config
from .models import mSubmission

# *****************************************************************************
def list(request):
    config.clog.dumpMethodInfo()
    qs = mSubmission.objects.all()
    vs = "<br>mSubmission.list: "

    if qs.count() == 0:
        vs += "No items to list"

    for item in qs:
        vs += item.name + ", "

    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vBase.main', xData=sessionKey)

# # *****************************************************************************
# def add(request, name):
#     config.clog.dumpMethodInfo()
#     vs = "<br>mSubmission.add: " + name
#     try:
#         mSubmission.objects.get(name=name)
#         vs += " already exists"
#     except ObjectDoesNotExist:
#         user = mSubmission(name=name, poi=True)
#         user.save()
#         vs += " added"
#
#     sessionKey = 'blue'
#     request.session[sessionKey] = vs
#     return redirect('vBase.main', xData=sessionKey)


# *****************************************************************************
def delAll(request):
    config.clog.dumpMethodInfo()
    vs = "<br>mSubmission.delAll: "

    qs = mSubmission.objects.all()
    vs += str(qs.count()) + " mSubmissions deleted"
    qs.delete()

    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vBase.main', xData=sessionKey)

# *****************************************************************************
def update():
    config.clog.dumpMethodInfo()
    config.clog.logger.info("=====================================================")


    subreddits = subreddit.objects.all()
    if subreddits.count() == 0:
        rv += "<BR> No subreddits found"
    else:
        for su in subreddits:
            argDict = {'rv': ""}
            blSubredditSubmissions_updateThreadsForSubreddits(su, argDict)
            rv += argDict['rv']
    config.clog.logger.info("=====================================================")
    return HttpResponse(rv)

















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


