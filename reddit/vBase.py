from django.http import HttpResponse
from django.shortcuts import redirect
import config

# *****************************************************************************
def main(request, xData=None):
    config.clog.dumpMethodInfo()

    vs  = 'vBase.main:'
    moreData = request.session.get(xData, '')
    vs += moreData

    vs += '<br><a href="http://localhost:8000/reddit/vUser/list">vUser list</a>'
    vs += '<br><a href="http://localhost:8000/reddit/vUser/add/OldDevLearningLinux">vUser add</a>'
    vs += '<br><a href="http://localhost:8000/reddit/vUser/delAll">vUser delAll</a>'
    return HttpResponse(vs)



