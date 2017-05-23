from celery import task
from datagrab.celery import app as celery_app               # for beat tasks
from celery.task.control import inspect                     # for ispectTasks
from celery.schedules import crontab                        # for crontab periodic tasks
from celery import current_task
from django.core.exceptions import ObjectDoesNotExist
from .config import clog
from .models import mcomment
from .models import msubreddit
from .models import mthread
from .models import muser
import pprint

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
def TASK_testLogLevels():
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)

    clog.logger.critical("%s: %-36s %10s:" % (current_task.request.id[:13], mi, 'critical'))
    clog.logger.error   ("%s: %-36s %10s:" % (current_task.request.id[:13], mi, 'error'))
    clog.logger.warning ("%s: %-36s %10s:" % (current_task.request.id[:13], mi, 'warning'))
    clog.logger.info    ("%s: %-36s %10s:" % (current_task.request.id[:13], mi, 'info'))
    clog.logger.debug   ("%s: %-36s %10s:" % (current_task.request.id[:13], mi, 'debug'))
    clog.logger.trace   ("%s: %-36s %10s:" % (current_task.request.id[:13], mi, 'trace'))
    return ""

# --------------------------------------------------------------------------
@task()
def TASK_updateUsersForAllComments(numberToProcess):
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)

    # create PRAW prawReddit instance
    prawReddit = mcomment.getPrawRedditInstance()
    countUsersAdded = 0

    qs = mcomment.objects.filter(puseradded=False)
    clog.logger.info("%s: %-36s %10s: %d comments to be updated" % (current_task.request.id[:13], mi, 'processing',  qs.count()))
    while qs.count() > 0:

        # Look at first result
        i_mcomment = qs[0]

        # AddOrUpdate that user
        prawRedditor = prawReddit.redditor(i_mcomment.username)
        i_muser = muser.objects.addOrUpdate(prawRedditor)

        if i_muser.addOrUpdateTempField == "new":
            countUsersAdded += 1

        # set puseradded True for any false comments for that user
        qs2 = mcomment.objects.filter(puseradded=False).filter(username=i_mcomment.username)
        for item in qs2:
            item.puseradded = True
            item.save()

        # are there any puseradded False comments left
        qs = mcomment.objects.filter(puseradded=False)

        numberToProcess -= 1
        if numberToProcess <= 0:
            break

    clog.logger.info("%s: %-36s %10s: %d comments to be updated, %d users added" % (current_task.request.id[:13], mi, 'completed',   qs.count(), countUsersAdded))
    return ""

# --------------------------------------------------------------------------
heartbeatTickString = "Tick"
@celery_app.task
def TASK_inspectTaskQueue():
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)

    thisTaskName    = 'reddit.tasks.TASK_inspectTaskQueue'
    workerName      = "celery@datagrab"

    i = inspect()

    # clog.logger.info("scheduled: %s" % (pprint.pformat(i.scheduled())))
    # clog.logger.info("active: %s" % (pprint.pformat(i.active())))
    # clog.logger.info("reserved: %s" % (pprint.pformat(i.reserved())))

    # Scheduled Tasks
    scheduledCount = 0
    scheduled = i.scheduled()
    if len(scheduled) > 0 and workerName in scheduled:
        scheduledList = scheduled[workerName]
        for item in scheduledList:
            if item['name'] != thisTaskName:    # Ignore THIS task
                scheduledCount += 1

    # Active Tasks
    activeCount = 0
    active = i.active()
    if len(active) > 0 and workerName in active:
        activeList = active[workerName]
        for item in activeList:
            if item['name'] != thisTaskName:    # Ignore THIS task
                activeCount += 1

    # Reserved Tasks
    reservedCount = 0
    reserved = i.reserved()
    if len(reserved) > 0 and workerName in reserved:
        reservedList = reserved[workerName]
        for item in reservedList:
            if item['name'] != thisTaskName:    # Ignore THIS task
                reservedCount += 1

    global heartbeatTickString
    if scheduledCount or activeCount or reservedCount:
        clog.logger.info("%s: %-36s %10s: %d active, %d scheduled, %d reserved" % (current_task.request.id[:13], mi, heartbeatTickString, activeCount, scheduledCount, reservedCount))
    else:
        clog.logger.info("%s: %-36s %10s: No tasks pending" % (current_task.request.id[:13], mi, heartbeatTickString))
    if heartbeatTickString == 'Tick': heartbeatTickString = 'Tok'
    else:                             heartbeatTickString = 'Tick'

    return ""

# --------------------------------------------------------------------------
@task()
def TASK_template():
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)

    # # create PRAW prawReddit instance
    # prawReddit = mcomment.getPrawRedditInstance()

    clog.logger.info("%s: %-36s %10s:" % (current_task.request.id[:13], mi, 'processing'))

    clog.logger.info("%s: %-36s %10s:" % (current_task.request.id[:13], mi, 'completed'))
    return ""

# --------------------------------------------------------------------------
@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task( 5.0,      TASK_testLogLevels.s())
    sender.add_periodic_task(60.0,      TASK_inspectTaskQueue.s())
    sender.add_periodic_task(10.0,      TASK_updateUsersForAllComments.s(50))
    sender.add_periodic_task( 5.0,      TASK_template.s())






    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )










