from django.http import HttpResponse
from django.shortcuts import redirect
from ..config import clog
from ..models import mcomment, msubreddit, mthread, muser
from ..tasks.tmisc import TASK_generateModelCountData
# import pprint

# *****************************************************************************
def main(request, xData=None):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = '<b>vuser</b>:'
    vs += ' <a href="http://localhost:8000/reddit/vuser/list">list</a>'
    vs += ', <b>add</b> <a href="http://localhost:8000/reddit/vuser/formNewPoiUser">newPoiUser</a>'

    vs += '<br><b>vsubreddit</b>:'
    vs += ' <a href="http://localhost:8000/reddit/vsubreddit/list">list</a>'
    vs += ', <b>add</b> <a href="http://localhost:8000/reddit/vsubreddit/formNewPoiSubreddit">newPoiSubreddit</a>'

    # vs += ', <a href="http://localhost:8000/reddit/vuser/delAll">delAll</a>'
    # vs += ', <a href="http://localhost:8000/reddit/vsubreddit/delAll">delAll</a>'
    # vs += '  <a href="http://localhost:8000/reddit/vthread/delAll">delAll</a>'

    vs += displayDatabaseModelCounts()
    vs += '<br><a href="http://localhost:8000/reddit/vbase/test">vbase.test</a>'
    vs += '<BR>============================'

    vs += '<br>' + request.session.get(xData, '')
    return HttpResponse(vs)

# *****************************************************************************
def displayDatabaseModelCounts():
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)

    listOfModelCountStrings = TASK_generateModelCountData()

    s = '<BR>============================'
    s += '<font face="Courier New" color="green">'
    for line in listOfModelCountStrings:
        s += '<BR>'
        s += line.replace(" ", "&nbsp;")
    s += '</font>'
    s += '<BR>============================'
    return s

# *****************************************************************************
def test(request):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = "vbase.test: EMPTY TEST"

    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)





