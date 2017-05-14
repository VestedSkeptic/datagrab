from django.http import HttpResponse
from django.shortcuts import redirect
from ..config import clog

# *****************************************************************************
def main(request, xData=None):
    clog.dumpMethodInfo()

    vs  = 'vbase.main:'
    moreData = request.session.get(xData, '')
    vs += moreData

    vs += '<br><b>vuser</b>:'
    vs += ' <a href="http://localhost:8000/reddit/vuser/list">list</a>'
    vs += ' <a href="http://localhost:8000/reddit/vuser/add/OldDevLearningLinux">add</a>'
    vs += ' <a href="http://localhost:8000/reddit/vuser/delAll">delAll</a>'

    vs += '<br><b>vsubreddit</b>:'
    vs += ' <a href="http://localhost:8000/reddit/vsubreddit/list">list</a>'
    vs += ' <a href="http://localhost:8000/reddit/vsubreddit/add/Molw">add</a>'
    vs += ' <a href="http://localhost:8000/reddit/vsubreddit/delAll">delAll</a>'
    vs += ' <a href="http://localhost:8000/reddit/vsubreddit/update">update</a>'

    vs += '<br><b>vthread</b>:'
    vs += ' <a href="http://localhost:8000/reddit/vthread/list">list</a>'
    vs += ' <a href="http://localhost:8000/reddit/vthread/delAll">delAll</a>'

    return HttpResponse(vs)



