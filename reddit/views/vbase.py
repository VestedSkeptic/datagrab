from django.http import HttpResponse
from django.shortcuts import redirect
from ..config import clog
from ..models import mcomment, msubreddit, mthread, muser
# import pprint

# *****************************************************************************
def main(request, xData=None):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = '<b>vuser</b>:'
    vs += ' <a href="http://localhost:8000/reddit/vuser/list">list</a>'
    vs += ', <b>add</b>:'
    vs += ' <a href="http://localhost:8000/reddit/vuser/add/OldDevLearningLinux">OldDevLearningLinux</a>'
    vs += ', <a href="http://localhost:8000/reddit/vuser/add/RoadsideBandit">RoadsideBandit</a>'

    vs += '<br><b>vsubreddit</b>:'
    vs += ' <a href="http://localhost:8000/reddit/vsubreddit/list">list</a>'
    vs += ' <b>add</b>: '
    vs += ' <a href="http://localhost:8000/reddit/vsubreddit/add/Molw">Molw</a>'
    vs += ', <a href="http://localhost:8000/reddit/vsubreddit/add/politics">Politics</a>'

    vs += '<br><b>vthread</b>:'
    vs += ' <b>list</b>:'
    vs += ' <a href="http://localhost:8000/reddit/vthread/list/Molw">Molw</a>'
    vs += ', <a href="http://localhost:8000/reddit/vthread/list/politics">Politics</a>'

    vs += '<br><b>vanalysis</b>:'
    vs += '<br><b>poiUsersOfSubreddit</b>:'
    vs += ' <a href="http://localhost:8000/reddit/vanalysis/poiUsersOfSubreddit/The_Donald/500">The_Donald</a>'
    vs += '<br><b>moderatorsOfSubreddit</b>:'
    vs += ' <a href="http://localhost:8000/reddit/vanalysis/moderatorsOfSubreddit/The_Donald">The_Donald</a>'




    # vs += ', <a href="http://localhost:8000/reddit/vuser/delAll">delAll</a>'
    # vs += ', <a href="http://localhost:8000/reddit/vsubreddit/delAll">delAll</a>'
    # vs += '  <a href="http://localhost:8000/reddit/vthread/delAll">delAll</a>'

    vs += displayDatabaseModelCounts()
    vs += '<br><a href="http://localhost:8000/reddit/vbase/test">vbase.test</a>'
    vs += '<BR>==========================='

    vs += '<br>' + request.session.get(xData, '')
    return HttpResponse(vs)

# *****************************************************************************
def displayDatabaseModelCounts():
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)

    users_poi               = muser.objects.filter(ppoi=True).count()
    users_notPoi            = muser.objects.filter(ppoi=False).count()
    users_ci                = mcomment.objects.filter(pdeleted=False).count()
    users_ci_deleted        = mcomment.objects.filter(pdeleted=True).count()
    subreddits              = msubreddit.objects.all().count()
    subreddits_si           = mthread.objects.filter(pdeleted=False).count()
    subreddits_si_deleted   = mthread.objects.filter(pdeleted=True).count()
    s = '<BR>==========================='
    s += '<BR>musers: ppoi = ' + str(users_poi)
    s += ', !ppoi = ' + str(users_notPoi)
    s += '<BR>mcomments = ' + str(users_ci)
    s += ', deleted = ' + str(users_ci_deleted)
    s += '<BR>msubreddits = ' + str(subreddits)
    s += '<BR>mthreads = ' + str(subreddits_si)
    s += ', deleted = ' + str(subreddits_si_deleted)
    s += '<BR>==========================='
    return s

# *****************************************************************************
def test(request):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = "vbase.test: EMPTY TEST"

    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)








