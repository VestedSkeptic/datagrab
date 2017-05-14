from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from ..config import clog
from ..models import muser

# *****************************************************************************
def list(request):
    clog.dumpMethodInfo()
    qs = muser.objects.all()
    vs = "<br>muser.list: "

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
    vs = "<br>muser.add: " + name
    try:
        muser.objects.get(name=name)
        vs += " already exists"
    except ObjectDoesNotExist:
        user = muser(name=name, poi=True)
        user.save()
        vs += " added"

    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)


# *****************************************************************************
def delAll(request):
    clog.dumpMethodInfo()
    vs = "<br>muser.delAll: "

    qs = muser.objects.all()
    vs += str(qs.count()) + " musers deleted"
    qs.delete()

    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)





























