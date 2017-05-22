from django.http import HttpResponse
from django.shortcuts import redirect
# from django.core.exceptions import ObjectDoesNotExist
from ..config import clog
# from ..models import msubreddit
from ..tasks import task_commentsUpdateUsers
# import praw
# import pprint

# *****************************************************************************
def updateUsers(request):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = ''
    task_commentsUpdateUsers.delay()

    clog.logger.info(vs)
    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)


























