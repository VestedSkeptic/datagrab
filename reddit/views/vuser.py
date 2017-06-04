from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from ..config import clog
from ..models import muser
from ..forms import fuser
# import pprint

# *****************************************************************************
def list(request, xData=None):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    qs = muser.objects.filter(ppoi=True).order_by('name')
    return render(request, 'vuser_list.html', {'users': qs, 'rightCol': mark_safe(request.session.get(xData, ''))})

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
def formNewPoiUser(request):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    if request.method == 'POST':                # if this is a POST request we need to process the form data
        form = fuser.fNewPoiUser(request.POST)  # create a form instance and populate it with data from the request:
        if form.is_valid():                     # check whether it's valid:
            # process the data in form.cleaned_data as required
            # pprint.pprint(form.cleaned_data)

            # add user as poi
            prawReddit = muser.getPrawRedditInstance()
            prawRedditor = prawReddit.redditor(form.cleaned_data['poiUser'])

            i_muser = muser.objects.addOrUpdate(prawRedditor)
            i_muser.ppoi = True
            i_muser.save()

            vs = form.cleaned_data['poiUser']
            if i_muser.addOrUpdateTempField == "new": vs += ' poi user added.'
            else:                                     vs += ' poi user already existed.'

            clog.logger.info(vs)
            sessionKey = 'blue'
            request.session[sessionKey] = vs
            return redirect('vbase.main', xData=sessionKey)
    else:                                       # if a GET (or any other method) we'll create a blank form
        form = fuser.fNewPoiUser()

    return render(request, 'fSimpleSubmitForm.html', {'form': form})




















