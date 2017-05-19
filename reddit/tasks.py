from celery import task
from .config import clog
from .blue import bthread
from .models import msubreddit
from django.core.exceptions import ObjectDoesNotExist

# --------------------------------------------------------------------------
@task()
def task_getMoreThreadsForSubredditName(subredditName):
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)

    try:
        i_msubreddit = msubreddit.objects.get(name=subredditName)
        bthread.getMoreThreadsForSubredditInstance(i_msubreddit=i_msubreddit)
        return "yes"
    except ObjectDoesNotExist:
        clog.logger.info("%s: subreddit %s does not exist" % (mi, subredditName))
        return "no"


### PROCESS ###
# 1. Start Django Server Terminal

#### WORKER SHELL Celery 4.0 ####
# 2. Start Celery Worker Terminal
# note: kill with Ctrl-C  Ctrl-C
# note: kill and restart for any code change
# note: for production worker should be run as daemon
# celery -A datagrab worker -l info


















