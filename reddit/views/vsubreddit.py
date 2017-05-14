from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from ..config import clog
from ..models import msubreddit

# *****************************************************************************
def list(request):
    clog.dumpMethodInfo()
    qs = msubreddit.objects.all()
    vs = "<br>msubreddit.list: "

    if qs.count() == 0:
        vs += "No items to list"

    for item in qs:
        vs += item.name + ", "

    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)

# *****************************************************************************
def add(request, name):
    clog.dumpMethodInfo()
    vs = "<br>msubreddit.add: " + name
    try:
        msubreddit.objects.get(name=name)
        vs += " already exists"
    except ObjectDoesNotExist:
        user = msubreddit(name=name, poi=True)
        user.save()
        vs += " added"

    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)


# *****************************************************************************
def delAll(request):
    clog.dumpMethodInfo()
    vs = "<br>msubreddit.delAll: "

    qs = msubreddit.objects.all()
    vs += str(qs.count()) + " msubreddits deleted"
    qs.delete()

    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)

# *****************************************************************************
def update(request):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = mi

    qs = msubreddit.objects.all()
    if qs.count() > 0:
        for iSubreddit in qs:
            argDict = {'vs': ""}
            iSubreddit.updateThreads(argDict)
            vs += argDict['vs']
    else:
        vs += " No msubreddits found"

    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)


























