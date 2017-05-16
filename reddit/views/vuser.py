from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from ..config import clog
from ..models import muser
from ..blue import bcomment
import praw
import pprint

# *****************************************************************************
def list(request):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = ''
    qs = muser.objects.all()
    if qs.count() == 0:
        vs += "No items to list"
    for item in qs:
        vs += item.name + ", "

    clog.logger.info(vs)
    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)

# *****************************************************************************
def add(request, name):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = name

    prawReddit = muser.getPrawRedditInstance()
    prawRedditor = prawReddit.redditor(name)

    i_muser = muser.objects.addOrUpdate(prawRedditor)
    clog.logger.debug("i_muser = %s" % (pprint.pformat(vars(i_muser))))

    if i_muser.addOrUpdateTempField == "new":           vs += " added"
    if i_muser.addOrUpdateTempField == "oldUnchanged":  vs += " oldUnchanged"
    if i_muser.addOrUpdateTempField == "oldChanged":    vs += " oldChanged"

    clog.logger.info(vs)
    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)

# *****************************************************************************
def delAll(request):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = ''
    qs = muser.objects.all()
    vs += str(qs.count()) + " musers deleted"
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
    qs = muser.objects.all()
    if qs.count() > 0:
        for i_muser in qs:
            argDict = {'vs': ""}
            # i_muser.updateThreads(argDict)
            bcomment.updateUserComments(i_muser)
            vs += argDict['vs']
    else:
        vs += " No musers found"

    clog.logger.info(vs)
    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)


























