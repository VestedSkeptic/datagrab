from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from ..config import clog
from ..models import msubreddit
from ..blue import bthread

# *****************************************************************************
def list(request):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = ''
    qs = msubreddit.objects.all()
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
        msubreddit.objects.get(name=name)
        vs += "already exists"
    except ObjectDoesNotExist:
        user = msubreddit(name=name, poi=True)
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
    qs = msubreddit.objects.all()
    vs += str(qs.count()) + " msubreddits deleted"
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
    qs = msubreddit.objects.all()
    if qs.count() > 0:
        vs += "%d msubreddits found" % (qs.count())
        for i_msubreddit in qs:
            argDict = {'vs': ""}
            bthread.updateSubredditThreads(i_msubreddit)
            vs += argDict['vs']
    else:
        vs += "No msubreddits found"

    clog.logger.info(vs)
    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)


























