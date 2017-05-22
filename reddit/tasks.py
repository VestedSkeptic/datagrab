from celery import task
from django.core.exceptions import ObjectDoesNotExist
from .config import clog
from .models import mcomment
from .models import msubreddit
from .models import mthread
from .models import muser

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
    # clog.logger.info(mi)

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
        clog.logger.info("%s: thread %s does not exist" % (mi, username))
        clog.logger.info("********* FAIL *********")
        return "********* FAIL *********"


# --------------------------------------------------------------------------
@task()
def task_commentsUpdateUsers():
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)

    # qs = mcomment.objects.filter(puseradded=False)
    # if qs.count() == 0:
    #     clog.logger.info("********* No comments to update *********")
    #     return "********* No comments to update *********"
    # else:
    #     clog.logger.info("%d comments found with puseradded = False" % (qs.count()))
    #     for i_mcomment in qs:
    #         i_mcomment.updateUser()
    #     clog.logger.info("********* PASS *********")
    #     return "********* PASS *********"

    # create PRAW prawReddit instance
    prawReddit = mcomment.getPrawRedditInstance()

    qs = mcomment.objects.filter(puseradded=False)
    while qs.count() > 0:
        clog.logger.info("%d comments found with puseradded = False" % (qs.count()))

        # Look at first result
        i_mcomment = qs[0]

        # AddOrUpdate that user
        prawRedditor = prawReddit.redditor(i_mcomment.username)
        i_muser = muser.objects.addOrUpdate(prawRedditor)

        # if i_muser.addOrUpdateTempField == "new":
        #     clog.logger.info("%s: user %s created" % (mi, i_muser.name))

        # set puseradded True for any false comments for that user
        qs2 = mcomment.objects.filter(puseradded=False).filter(username=i_mcomment.username)
        for item in qs2:
            item.puseradded = True
            item.save()

        # are there any puseradded False comments left
        qs = mcomment.objects.filter(puseradded=False)

    clog.logger.info("********* PASS *********")
    return "********* PASS *********"





# --------------------------------------------------------------------------
### PROCESS ###
# 1. Start Django Server Terminal

#### WORKER SHELL Celery 4.0 ####
# 2. Start Celery Worker Terminal
# note: kill with Ctrl-C  Ctrl-C
# note: kill and restart for any code change
# note: for production worker should be run as daemon
# celery -A datagrab worker -l CRITICAL -f /home/delta/work/logs/worker.txt

















