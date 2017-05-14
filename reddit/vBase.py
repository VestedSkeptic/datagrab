from django.http import HttpResponse
from django.shortcuts import redirect
import config

# *****************************************************************************
def main(request, xData=None):
    config.clog.dumpMethodInfo()

    vs  = 'vBase.main:'
    moreData = request.session.get(xData, '')
    vs += moreData

    vs += '<br><b>vUser</b>:'
    vs += ' <a href="http://localhost:8000/reddit/vUser/list">list</a>'
    vs += ' <a href="http://localhost:8000/reddit/vUser/add/OldDevLearningLinux">add</a>'
    vs += ' <a href="http://localhost:8000/reddit/vUser/delAll">delAll</a>'

    vs += '<br><b>vSubreddit</b>:'
    vs += ' <a href="http://localhost:8000/reddit/vSubreddit/list">list</a>'
    vs += ' <a href="http://localhost:8000/reddit/vSubreddit/add/Molw">add</a>'
    vs += ' <a href="http://localhost:8000/reddit/vSubreddit/delAll">delAll</a>'
    vs += ' <a href="http://localhost:8000/reddit/vSubreddit/update">update</a>'

    vs += '<br><b>vThread</b>:'
    vs += ' <a href="http://localhost:8000/reddit/vThread/list">list</a>'
    vs += ' <a href="http://localhost:8000/reddit/vThread/delAll">delAll</a>'

    return HttpResponse(vs)



