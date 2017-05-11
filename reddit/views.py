from django.http import HttpResponse
from .blUserComments import blUserComments_updateForAllUsers, getHierarchyOfCommentsAtLevel, blUserComments_deleteAll, blUserComments_addUser
from .blSubredditSubmissions import blSubredditSubmissions_updateForAllSubreddits, blSubredditSubmissions_deleteAllSubreddits, blSubredditSubmissions_addSubreddit, blSubredditSubmissions_deleteAll_SSFE, blSubredditSubmissions_updateAll_SSFE
from .blSubmissionComments import blSubmissionComments_updateForAllSubmissions
from .models import *

# *****************************************************************************
def main(request):
    s  = ''
    s += '<br><a href="http://localhost:8000/admin/reddit/">admin</a>'
    s += '<br><a href="http://localhost:8000/reddit/praw/ucfau/">update user comments</a>'
    s += '<br><a href="http://localhost:8000/reddit/praw/usfas/">update subreddit submissions</a>'
    s += '<br><a href="http://localhost:8000/reddit/praw/ucfas/">update submission comments</a>'

    s += '<br><br><b>ParseCommentHeirarchy: </b>'
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

    s += '<br>'
    s += '<br><a href="http://localhost:8000/reddit/praw/usrsfe/">update subredditSubmissionFieldsExtracted</a>'

    s += '<br>' + displayDatabaseModelCounts()

    s += '<br><b>Delete: '
    s += ' <a href="http://localhost:8000/reddit/praw/dau/">users</a>'
    s += ' <a href="http://localhost:8000/reddit/praw/das/">subreddits</a>'
    s += ' <a href="http://localhost:8000/reddit/praw/da/">all</a>'
    s += '<br><b>Add: '
    s += ' <a href="http://localhost:8000/reddit/praw/auser/OldDevLearningPython">user OldDevLearningPython</a>'
    s += ' <a href="http://localhost:8000/reddit/praw/asub/molw">subreddit molw</a>'
    s += ' <a href="http://localhost:8000/reddit/praw/aboth/OldDevLearningPython/molw">both</a>'
    s += '<br><b>Delete: '
    s += ' <a href="http://localhost:8000/reddit/praw/ssfe/">subredditSubmissionFieldsExtracted</a>'
    # s += ' <a href="http://localhost:8000/reddit/praw/das/">subreddits</a>'
    # s += ' <a href="http://localhost:8000/reddit/praw/da/">all</a><br>'
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
    s = blUserComments_deleteAll()
    return HttpResponse(s)

# *****************************************************************************
def deleteAllSubreddits(request):
    s = blSubredditSubmissions_deleteAllSubreddits()
    return HttpResponse(s)

# *****************************************************************************
def deleteAll(request):
    s = blUserComments_deleteAll()
    s += "<br>"
    s += blSubredditSubmissions_deleteAllSubreddits()
    return HttpResponse(s)

# *****************************************************************************
def parseCommentHeirarchy(request, hLevel):

    # for testing purposes get submissionIndex with MOST number of comments
    sIndex = subredditSubmissionIndex.objects.filter(cForestGot=True).order_by('-count')

    for item in sIndex:
        s = getHierarchyOfCommentsAtLevel(item.name, int(hLevel))
        break # as we are only doing one item for now

    return HttpResponse(s)

# *****************************************************************************
def addUser(request, uname):
    s = blUserComments_addUser(uname)
    return HttpResponse(s)

# *****************************************************************************
def addSub(request, sname):
    s = blSubredditSubmissions_addSubreddit(sname)
    return HttpResponse(s)

# *****************************************************************************
def addBoth(request, uname, sname):
    s = blUserComments_addUser(uname)
    s += "<br>"
    s += blSubredditSubmissions_addSubreddit(sname)
    return HttpResponse(s)

# *****************************************************************************
def deleteAllSSFE(request):
    s = blSubredditSubmissions_deleteAll_SSFE()
    return HttpResponse(s)

# *****************************************************************************
def updateSSFE(request):
    s = blSubredditSubmissions_updateAll_SSFE()
    return HttpResponse(s)






