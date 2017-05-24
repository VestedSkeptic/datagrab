from django.http import HttpResponse
from django.shortcuts import redirect
from ..config import clog
from ..models import mcomment, msubreddit, mthread, muser
# import pprint

# *****************************************************************************
def main(request, xData=None):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = request.session.get(xData, '')

    vs += '<br><a href="http://localhost:8000/reddit/vbase/test">vbase.test</a>'
    vs += '<br><b>vuser</b>:'
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

    # vs += ', <a href="http://localhost:8000/reddit/vuser/delAll">delAll</a>'
    # vs += ', <a href="http://localhost:8000/reddit/vsubreddit/delAll">delAll</a>'
    # vs += '  <a href="http://localhost:8000/reddit/vthread/delAll">delAll</a>'


    vs += '<br>' + displayDatabaseModelCounts()
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
    s = ''
    s += '<BR>==========================='
    s += '<BR>musers: ppoi = ' + str(users_poi)
    s += ', !ppoi = ' + str(users_notPoi)
    s += '<BR>mcomments = ' + str(users_ci)
    s += ', deleted = ' + str(users_ci_deleted)
    s += '<BR>msubreddits = ' + str(subreddits)
    s += '<BR>mthreads = ' + str(subreddits_si)
    s += ', deleted = ' + str(subreddits_si_deleted)
    s += '<BR>==========================='
    s += '<BR>'
    return s

# # *****************************************************************************
# def test(request):
#     mi = clog.dumpMethodInfo()
#     clog.logger.info(mi)
#
#     vs = "vbase.test: EMPTY TEST"
#
#     sessionKey = 'blue'
#     request.session[sessionKey] = vs
#     return redirect('vbase.main', xData=sessionKey)



# *****************************************************************************
from django.db.models import Count
def test(request):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = "vbase.test: EMPTY TEST"

    # subPoi = 't5_38unr'        # TD
    # prawReddit = mcomment.getPrawRedditInstance()
    # subredditDict = {}
    #
    # # Get a list of users who've posted in TD and sort this by number of comments
    # qs = mcomment.objects.filter(subreddit=subPoi).values('username').annotate(num_count=Count('username')).order_by('-num_count')
    # for userPoi in qs:
    #     if userPoi['num_count'] >= 896:
    #         # # {'num_count': 785, 'username': 'deleted'}
    #         # print(userPoi)
    #
    #         # # Add this user as poi
    #         # prawRedditor = prawReddit.redditor(userPoi['username'])
    #         # i_muser = muser.objects.addOrUpdate(prawRedditor)
    #         # i_muser.ppoi = True
    #         # i_muser.save()
    #         # print("%s added" % (userPoi['username']))
    #
    #
    # #         # # Get subreddits this person also comments in
    # #         qs2 = mcomment.objects.filter(username=userPoi['username']).values('rsubreddit_name_prefixed').annotate(num_count2=Count('rsubreddit_name_prefixed')).order_by('-num_count2')
    # #         for jj in qs2:
    # #             if jj['rsubreddit_name_prefixed'] not in subredditDict:
    # #                 subredditDict[jj['rsubreddit_name_prefixed']] = 0
    # #             subredditDict[jj['rsubreddit_name_prefixed']] += jj['num_count2']
    # #
    # #
    # # for k in subredditDict:
    # #     clog.logger.info("%06d: %s" % (subredditDict[k], k))
    #
    # sessionKey = 'blue'
    # request.session[sessionKey] = vs
    # return redirect('vbase.main', xData=sessionKey)







