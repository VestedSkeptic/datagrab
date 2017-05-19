from celery import task
from .config import clog
from .models import msubreddit
from django.core.exceptions import ObjectDoesNotExist

# --------------------------------------------------------------------------
@task()
def task_getMoreThreadsForSubredditName(subredditName):
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)

    try:
        i_msubreddit = msubreddit.objects.get(name=subredditName)
        i_msubreddit.updateThreads()
        return "yes"
    except ObjectDoesNotExist:
        clog.logger.info("%s: subreddit %s does not exist" % (mi, subredditName))
        return "no"

# --------------------------------------------------------------------------
@task()
def task_testLogLevels():
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)
    clog.logger.critical("critical")
    clog.logger.error("error")
    clog.logger.warning("warning")
    clog.logger.info("info")
    clog.logger.debug("debug")
    clog.logger.trace("trace")





# --------------------------------------------------------------------------
### PROCESS ###
# 1. Start Django Server Terminal

#### WORKER SHELL Celery 4.0 ####
# 2. Start Celery Worker Terminal
# note: kill with Ctrl-C  Ctrl-C
# note: kill and restart for any code change
# note: for production worker should be run as daemon
# celery -A datagrab worker -l CRITICAL -f /home/delta/work/logs/worker.txt

















