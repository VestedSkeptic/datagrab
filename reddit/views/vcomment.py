# from django.http import HttpResponse
from django.shortcuts import redirect
from ..config import clog
from ..tasks import TASK_updateUsersForAllComments
# from django.core.exceptions import ObjectDoesNotExist
# from ..models import msubreddit
# import praw
# import pprint

# *****************************************************************************
def updateUsers(request):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = ''
    TASK_updateUsersForAllComments.delay()

    clog.logger.info(vs)
    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)


























