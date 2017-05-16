from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from ..config import clog
from ..models import mthread
from ..blue import bcomment

# *****************************************************************************
def list(request):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = ''
    qs = mthread.objects.all()
    if qs.count() == 0:
        vs += "No items to list"
    for item in qs:
        vs += item.name
        vs += ": rauthor = " + item.rauthor
        vs += ", rdowns = " + str(item.rdowns)
        vs += ", rups = " + str(item.rups)
        vs += ", rtitle = " + item.rtitle
        vs += ", ris_self = " + str(item.ris_self)
        vs += ", rselftext = " + item.rselftext

    clog.logger.info(vs)
    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)

# *****************************************************************************
def delAll(request):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = ''
    qs = mthread.objects.all()
    vs += str(qs.count()) + " mSubmissions deleted"
    qs.delete()

    clog.logger.info(vs)
    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)

# *****************************************************************************
def update(request):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = ''
    qs = mthread.objects.filter(pdeleted=False).order_by('subreddit__name')
    if qs.count() > 0:
        for i_mthread in qs:
            argDict = {'rv': "", 'modeCount': {'Comment Forest New' : 0, 'Comment Forest Old' : 0, 'Method To Be Implemented Later' : 0, }}
            bcomment.updateThreadComments(i_mthread, argDict)

        s_temp = "Comment Forest New count" + " = " + str(argDict['modeCount']['Comment Forest New'])
        clog.logger.info(s_temp)
        s_temp = "Comment Forest Old count" + " = " + str(argDict['modeCount']['Comment Forest Old'])
        clog.logger.info(s_temp)
        s_temp = "Method To Be Implemented Later count" + " = " + str(argDict['modeCount']['Method To Be Implemented Later'])
        clog.logger.info(s_temp)
    else:
        vs += " No mthreads found"

    clog.logger.info(vs)
    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)











