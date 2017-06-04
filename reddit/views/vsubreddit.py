from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from ..config import clog
from ..models import msubreddit
from ..forms import fsubreddit
# import pprint

# *****************************************************************************
def list(request, xData=None):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    qs = msubreddit.objects.all().order_by('name')
    return render(request, 'vsubreddit_list.html', {'subreddits': qs, 'rightCol': mark_safe(request.session.get(xData, ''))})

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
def formNewPoiSubreddit(request):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    if request.method == 'POST':                            # if this is a POST request we need to process the form data
        form = fsubreddit.fNewPoiSubreddit(request.POST)    # create a form instance and populate it with data from the request:
        if form.is_valid():                                 # check whether it's valid:
            # process the data in form.cleaned_data as required
            # pprint.pprint(form.cleaned_data)

            # add subreddit as poi
            prawReddit = msubreddit.getPrawRedditInstance()
            prawSubreddit = prawReddit.subreddit(form.cleaned_data['poiSubreddit'])

            i_msubreddit = msubreddit.objects.addOrUpdate(form.cleaned_data['poiSubreddit'], prawSubreddit)
            i_msubreddit.ppoi = True
            i_msubreddit.save()

            vs = form.cleaned_data['poiSubreddit']
            if i_msubreddit.addOrUpdateTempField == "new": vs += ' poi poiSubreddit added.'
            else:                                          vs += ' poi poiSubreddit already existed.'

            clog.logger.info(vs)
            sessionKey = 'blue'
            request.session[sessionKey] = vs
            return redirect('vbase.main', xData=sessionKey)
    else:                                                   # if a GET (or any other method) we'll create a blank form
        form = fsubreddit.fNewPoiSubreddit()

    return render(request, 'fSimpleSubmitForm.html', {'form': form})

























