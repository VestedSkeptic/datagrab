from celery import task
from django.core.exceptions import ObjectDoesNotExist
from .config import clog
from .models import msubreddit
from .models import muser
from .models import mthread

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
@task()
def task_subredditUpdateThreads(subredditName):
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)

    try:
        i_msubreddit = msubreddit.objects.get(name=subredditName)
        i_msubreddit.updateThreads()
        clog.logger.info("********* PASS *********")
        return "********* PASS *********"
    except ObjectDoesNotExist:
        clog.logger.info("%s: subreddit %s does not exist" % (mi, subredditName))
        clog.logger.info("********* FAIL *********")
        return "********* FAIL *********"

# --------------------------------------------------------------------------
@task()
def task_userUpdateComments(userName):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    try:
        i_muser = muser.objects.get(name=userName)
        i_muser.updateComments()
        clog.logger.info("********* PASS *********")
        return "********* PASS *********"
    except ObjectDoesNotExist:
        clog.logger.info("%s: user %s does not exist" % (mi, username))
        clog.logger.info("********* FAIL *********")
        return "********* FAIL *********"

# --------------------------------------------------------------------------
@task()
def task_threadUpdateComments(threadName):
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)

    try:
        i_mthread = mthread.objects.get(fullname=threadName)
        clog.logger.info("thread: %s" % (i_mthread.rtitle))
        i_mthread.updateComments()
        clog.logger.info("********* PASS *********")
        return "********* PASS *********"
    except ObjectDoesNotExist:
        clog.logger.info("%s: user %s does not exist" % (mi, username))
        clog.logger.info("********* FAIL *********")
        return "********* FAIL *********"



# --------------------------------------------------------------------------
### PROCESS ###
# 1. Start Django Server Terminal

#### WORKER SHELL Celery 4.0 ####
# 2. Start Celery Worker Terminal
# note: kill with Ctrl-C  Ctrl-C
# note: kill and restart for any code change
# note: for production worker should be run as daemon
# celery -A datagrab worker -l CRITICAL -f /home/delta/work/logs/worker.txt

















