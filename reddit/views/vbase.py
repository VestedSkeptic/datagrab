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

    vs += '<br><a href="http://localhost:8000/reddit/vbase/map">map</a>'

    # vs += ', <a href="http://localhost:8000/reddit/vuser/delAll">delAll</a>'
    # vs += ', <a href="http://localhost:8000/reddit/vsubreddit/delAll">delAll</a>'
    # vs += '  <a href="http://localhost:8000/reddit/vthread/delAll">delAll</a>'

    vs += displayDatabaseModelCounts()
    vs += '<br><a href="http://localhost:8000/reddit/vbase/test">vbase.test</a>'

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
def test(request):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = ''

    prawReddit = mcomment.getPrawRedditInstance()
    prawSubmissionObject = prawReddit.submission(id='6fvbyb')

    for duplicate in prawSubmissionObject.duplicates():
        vs += duplicate.subreddit_name_prefixed
        vs += ', '


    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)

# *****************************************************************************
def generateMapLink():
    vs = '<img src="'
    vs += "https://maps.googleapis.com/maps/api/staticmap?"

    # vs += "center=Quyon,Quebec"
    # vs += "center=45.529997,-76.12571597"       # compound
    vs += "center=45.53716674,-76.14626169"     # NW of compound, center of walking area

    vs += "&zoom=14"
    vs += "&size=1000x800"
    vs += "&maptype=roadmap"

    # vs += "&markers=color:blue%7Clabel:S%7C40.702147,-74.015794"
    # vs += "&markers=color:green%7Clabel:G%7C40.711614,-74.012318"
    # vs += "&markers=color:red%7Clabel:C%7C40.718217,-73.998284"

    vs += "&style=feature:road%7Celement:geometry%7Ccolor:0x000000&size=480x360"

    # my google api key
    # AIzaSyA3citi7wr_F-ACo-rScbUX1ViHdKN-RVM
    vs += "&key=AIzaSyA3citi7wr_F-ACo-rScbUX1ViHdKN-RVM"
    vs += '">'

    return vs

# *****************************************************************************
def map(request):
    vs = generateMapLink()
    return HttpResponse(vs)

