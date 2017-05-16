from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from ..config import clog
from ..models import muser
from ..blue import bcomment

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

    vs = name + ' '
    try:
        muser.objects.get(name=name)
        vs += "already exists"
    except ObjectDoesNotExist:
        user = muser(name=name, ppoi=True)
        user.save()
        vs += "added"

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


























