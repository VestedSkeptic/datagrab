from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from ..config import clog
from ..models import msubreddit
from ..tasks import task_subredditUpdateThreads
import praw
# import pprint

# *****************************************************************************
def list(request):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = ''
    qs = msubreddit.objects.all()
    if qs.count() == 0:
        vs += "No items to list"
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

    prawReddit = msubreddit.getPrawRedditInstance()
    prawSubreddit = prawReddit.subreddit(name)

    i_msubreddit = msubreddit.objects.addOrUpdate(name, prawSubreddit)
    i_msubreddit.ppoi = True
    i_msubreddit.save()
    # clog.logger.debug("i_msubreddit = %s" % (pprint.pformat(vars(i_msubreddit))))

    if i_msubreddit.addOrUpdateTempField == "new":             vs += " added"
    if i_msubreddit.addOrUpdateTempField == "oldUnchanged":    vs += " oldUnchanged"
    if i_msubreddit.addOrUpdateTempField == "oldChanged":      vs += " oldChanged"
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
    qs = msubreddit.objects.filter(ppoi=True)
    if qs.count() > 0:
        vs += "Scheduling task to update: "
        for i_msubreddit in qs:
            vs += i_msubreddit.name + ", "
            task_subredditUpdateThreads.delay(i_msubreddit.name)
    else:
        vs += "No msubreddits found"

    clog.logger.info(vs)
    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)


























