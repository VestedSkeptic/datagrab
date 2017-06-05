from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
# from django.utils.safestring import mark_safe
from ..config import clog
from ..models import mcomment
from ..forms import fuser
# import pprint

# *****************************************************************************
def user(request, username):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    # qs = mcomment.objects.filter(username=username).order_by('rcreated')
    # qs = mcomment.objects.filter(username=username).order_by('-rcreated')
    qs = mcomment.objects.filter(username=username).order_by('-rcreated_utc')
    return render(request, 'vcomment_user.html', {'comments': qs, 'username': username})

















