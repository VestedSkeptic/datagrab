from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from ..config import clog
from ..models import muser
from ..tasks import TASK_updateCommentsForUser
import praw
# import pprint

# *****************************************************************************
def list(request):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = ''
    qs = muser.objects.filter(ppoi=True)
    if qs.count() == 0:
        vs += "No users to list"
    for item in qs:
        vs += item.__str__() + ", "

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
    i_muser.ppoi = True
    i_muser.save()
    # clog.logger.debug("i_muser = %s" % (pprint.pformat(vars(i_muser))))

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
    qs = muser.objects.filter(ppoi=True)
    for i_muser in qs:
        clog.logger.info("=== Calling task TASK_updateCommentsForUser.delay for user %s" % (i_muser.name))
        TASK_updateCommentsForUser.delay(i_muser.name)

    clog.logger.info(vs)
    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)


























