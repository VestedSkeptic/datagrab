from celery import task
from datagrab.celery import app as celery_app               # for beat tasks
from celery.task.control import inspect                     # for ispectTasks
from django.core.exceptions import ObjectDoesNotExist
from .config import clog
from .models import mcomment
from .models import msubreddit
from .models import mthread
from .models import muser
import pprint

# --------------------------------------------------------------------------
@task()
def task_testLogLevels():
    mi = clog.dumpMethodInfo()

    clog.logger.info(mi)
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
heartbeatTickString = "Tick"
@celery_app.task
def inspectTaskQueue(arg):
    # clog.logger.info(arg)

    thisTaskName    = 'reddit.tasks.inspectTaskQueue'
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
    if scheduledCount or activeCount or reservedCount: clog.logger.info("*** %4s: Tasks: %d active, %d scheduled, %d reserved" % (heartbeatTickString, activeCount, scheduledCount, reservedCount))
    else:                                              clog.logger.info("*** %4s: No tasks pending" %(heartbeatTickString))

    if heartbeatTickString == 'Tick': heartbeatTickString = 'Tok'
    else:                             heartbeatTickString = 'Tick'



# Example of 'active' printout:
# {
#     'celery@datagrab':
#     [
#         {
#             'acknowledged': True,
#             'args': "('==== TASK QUEUE',)",
#             'delivery_info':
#             {
#                 'exchange': '',
#                 'priority': 0,
#                 'redelivered': None,
#                 'routing_key': 'celery'
#             },
#             'hostname': 'celery@datagrab',
#             'id': '3dcb76a3-8b6f-4227-a8a0-248921c83b37',
#             'kwargs': '{}',
#             'name': 'reddit.tasks.test',
#             'time_start': 10847.071408712,
#             'type': 'reddit.tasks.test',
#             'worker_pid': 11093
#         }
#     ]
# }


# --------------------------------------------------------------------------
@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, inspectTaskQueue.s('inspectTaskQueue'))










