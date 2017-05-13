from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
import config
from .models import mUser

# *****************************************************************************
def list(request):
    config.clog.dumpMethodInfo()
    qs = mUser.objects.all()
    vs = "<br>mUser.list: "

    if qs.count() == 0:
        vs += "No items to list"

    for item in qs:
        vs += item.name + ", "

    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vBase_main', xData=sessionKey)

# *****************************************************************************
def add(request, name):
    config.clog.dumpMethodInfo()
    vs = "<br>mUser.add: " + name
    try:
        mUser.objects.get(name=name)
        vs += " already exists"
    except ObjectDoesNotExist:
        user = mUser(name=name, poi=True)
        user.save()
        vs += " added"

    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vBase_main', xData=sessionKey)


# *****************************************************************************
def delAll(request):
    config.clog.dumpMethodInfo()
    vs = "<br>mUser.delAll: "

    qs = mUser.objects.all()
    vs += str(qs.count()) + " mUsers deleted"
    qs.delete()

    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vBase_main', xData=sessionKey)





























