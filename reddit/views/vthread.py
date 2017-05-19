from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger   # for pagination
from ..config import clog
from ..models import mthread

# *****************************************************************************
def delAll(request):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = ''
    qs = mthread.objects.all()
    vs += str(qs.count()) + " mSubmissions deleted"
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
    qs = mthread.objects.filter(pdeleted=False, pforestgot=False).order_by("-rcreated")
    if qs.count() > 0:
        count = 0
        for i_mthread in qs:
            count += 1
            clog.logger.info("Processing thread %d of %d" % (count, qs.count()))
            i_mthread.updateComments()
    else:
        vs += " No mthreads found"

    clog.logger.info(vs)
    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)

# *****************************************************************************
def list(request, subreddit):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    qs = mthread.objects.filter(subreddit__name=subreddit).order_by("-rcreated")
    paginator = Paginator(qs, 20) # Show 20 per page

    page = request.GET.get('page')
    try:
        threads = paginator.page(page)
    except PageNotAnInteger:
        threads = paginator.page(1) # If page is not an integer, deliver first page.
    except EmptyPage:
        threads = paginator.page(paginator.num_pages) # If page is out of range (e.g. 9999), deliver last page of results.

    return render(request, 'vthread_list.html', {'threads': threads, 'subreddit':subreddit})
























