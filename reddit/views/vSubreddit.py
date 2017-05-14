from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from ..config import clog
from ..models import mSubreddit

# *****************************************************************************
def list(request):
    clog.dumpMethodInfo()
    qs = mSubreddit.objects.all()
    vs = "<br>mSubreddit.list: "

    if qs.count() == 0:
        vs += "No items to list"

    for item in qs:
        vs += item.name + ", "

    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vBase.main', xData=sessionKey)

# *****************************************************************************
def add(request, name):
    clog.dumpMethodInfo()
    vs = "<br>mSubreddit.add: " + name
    try:
        mSubreddit.objects.get(name=name)
        vs += " already exists"
    except ObjectDoesNotExist:
        user = mSubreddit(name=name, poi=True)
        user.save()
        vs += " added"

    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vBase.main', xData=sessionKey)


# *****************************************************************************
def delAll(request):
    clog.dumpMethodInfo()
    vs = "<br>mSubreddit.delAll: "

    qs = mSubreddit.objects.all()
    vs += str(qs.count()) + " mSubreddits deleted"
    qs.delete()

    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vBase.main', xData=sessionKey)

# *****************************************************************************
def update(request):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = mi

    qs = mSubreddit.objects.all()
    if qs.count() > 0:
        for iSubreddit in qs:
            argDict = {'vs': ""}
            iSubreddit.updateThreads(argDict)
            vs += argDict['vs']
    else:
        vs += " No mSubreddits found"

    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vBase.main', xData=sessionKey)


























