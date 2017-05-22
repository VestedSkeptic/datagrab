from django.http import HttpResponse
from django.shortcuts import redirect
from ..config import clog
from ..models import mcomment, msubreddit, mthread, muser

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

    # clog.logger.critical("critical")
    # clog.logger.error("error")
    # clog.logger.warning("warning")
    # clog.logger.info("info")
    # clog.logger.debug("debug")
    # clog.logger.trace("trace")

    return s

# *****************************************************************************
def main(request, xData=None):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs  = ''
    moreData = request.session.get(xData, '')
    vs += moreData

    vs += '<br><b>vuser</b>: '
    vs += '  <a href="http://localhost:8000/reddit/vuser/list">list</a>'
    vs += ', <a href="http://localhost:8000/reddit/vuser/delAll">delAll</a>'
    vs += '<br><b>vuser add</b>: '
    vs += '  <a href="http://localhost:8000/reddit/vuser/add/OldDevLearningLinux">OldDevLearningLinux</a>'
    vs += ', <a href="http://localhost:8000/reddit/vuser/add/RoadsideBandit">RoadsideBandit</a>'

    vs += '<br><b>vsubreddit</b>: '
    vs += '  <a href="http://localhost:8000/reddit/vsubreddit/list">list</a>'
    vs += ', <a href="http://localhost:8000/reddit/vsubreddit/delAll">delAll</a>'
    vs += ' <b>add</b>: '
    vs += '  <a href="http://localhost:8000/reddit/vsubreddit/add/Molw">Molw</a>'
    vs += ', <a href="http://localhost:8000/reddit/vsubreddit/add/politics">Politics</a>'

    vs += '<br><b>vthread</b>:'
    vs += '  <a href="http://localhost:8000/reddit/vthread/delAll">delAll</a>'
    vs += '  <b>list</b>:'
    vs += '  <a href="http://localhost:8000/reddit/vthread/list/Molw">list Molw</a>'
    vs += ', <a href="http://localhost:8000/reddit/vthread/list/politics">list Politics</a>'

    vs += '<br><b>Tasks</b>:'
    vs += '<br><a href="http://localhost:8000/reddit/vsubreddit/update">Subreddit: update threads</a>'
    vs += '<br><a href="http://localhost:8000/reddit/vthread/update">Thread: update comments</a>'
    vs += '<br><a href="http://localhost:8000/reddit/comment/updateUsers">Comments: update users</a>'
    vs += '<br><br><a href="http://localhost:8000/reddit/vuser/update">User: update comments</a>'

    vs += '<br>' + displayDatabaseModelCounts()

    vs += '<br><a href="http://localhost:8000/reddit/vbase/test">vbase.test</a>'

    return HttpResponse(vs)

# # *****************************************************************************
# from ..tasks import task_testLogLevels
# def test(request):
#     mi = clog.dumpMethodInfo()
#     clog.logger.info(mi)
#
#     vs = "vbase.test: "
#
#     task_testLogLevels.delay()
#
#     clog.logger.info(vs)
#     sessionKey = 'blue'
#     request.session[sessionKey] = vs
#     return redirect('vbase.main', xData=sessionKey)

# # *****************************************************************************
# def test(request):
#     mi = clog.dumpMethodInfo()
#     clog.logger.info(mi)
#
#     vs = "vbase.test: update mcomment username field from user field"
#     qs = mcomment.objects.all()
#     if qs.count() == 0:
#         vs += "No comments found."
#     else:
#         for item in qs:
#             item.username = item.user.name;
#             item.save()
#         vs += str(qs.count()) + "comments updated"
#
#     clog.logger.info(vs)
#     sessionKey = 'blue'
#     request.session[sessionKey] = vs
#     return redirect('vbase.main', xData=sessionKey)

# *****************************************************************************
from django.db.models import Count
def test(request):
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)

    vs = "vbase.test: nothing here at the moment"

    subPoi = 't5_38unr'        # TD
    # qs = mcomment.objects.filter(subreddit=subPoi)
    # clog.logger.info("qs.count() = %d" % (qs.count()))

    prawReddit = mcomment.getPrawRedditInstance()

    subredditDict = {}

    # Get a list of users who've posted in TD and sort this by number of comments
    qs = mcomment.objects.filter(subreddit=subPoi).values('username').annotate(num_count=Count('username')).order_by('-num_count')
    for ii in qs:
        if ii['num_count'] > 50:
            # print(ii)
            # {'num_count': 785, 'username': 'deleted'}
            # {'num_count': 110, 'username': 'TheWhiteEnglishLion'}
            # {'num_count': 104, 'username': 'littleirishmaid'}
            # {'num_count': 102, 'username': 'journey345'}
            # {'num_count': 91, 'username': 'ActivatedJoeBot'}

            # prawRedditor = prawReddit.redditor(ii['username'])
            # i_muser = muser.objects.addOrUpdate(prawRedditor)
            # i_muser.ppoi = True
            # i_muser.save()


            # # Get subreddits this person also comments in
            qs2 = mcomment.objects.filter(username=ii['username']).values('rsubreddit_name_prefixed').annotate(num_count2=Count('rsubreddit_name_prefixed')).order_by('-num_count2')
            for jj in qs2:
                if jj['rsubreddit_name_prefixed'] not in subredditDict:
                    subredditDict[jj['rsubreddit_name_prefixed']] = 0
                subredditDict[jj['rsubreddit_name_prefixed']] += jj['num_count2']


    for k in subredditDict:
        clog.logger.info("%06d: %s" % (subredditDict[k], k))



    clog.logger.info(vs)
    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)

