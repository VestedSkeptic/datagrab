from celery import task
from celery.task.control import inspect                     # for ispectTasks
import time
from ..config import clog
from .tbase import getBaseP, getBaseC, getLine
from ..models import mcomment
from ..models import msubreddit
from ..models import mthread
from ..models import muser
# import pprint

# --------------------------------------------------------------------------
@task()
def TASK_template():
    mi = clog.dumpMethodInfo()
    ts = time.time()

    # # create PRAW prawReddit instance
    # prawReddit = mcomment.getPrawRedditInstance()

    clog.logger.info("%s" % (getBaseP(mi)))

    clog.logger.info("%s" % (getBaseC(mi, ts)))
    return ""

# --------------------------------------------------------------------------
heartbeatTickString = "TICK"
@task()
def TASK_inspectTaskQueue():
    mi = clog.dumpMethodInfo()
    ts = time.time()

    thisTaskName    = 'reddit.tasks.tmisc.TASK_inspectTaskQueue'
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
    if heartbeatTickString == 'TICK': heartbeatTickString = 'tock'
    else:                             heartbeatTickString = 'TICK'

    if scheduledCount or activeCount or reservedCount:
        clog.logger.info("%s %s: %d active, %d scheduled, %d reserved" % (getBaseC(mi, ts), heartbeatTickString, activeCount, scheduledCount, reservedCount))
    else:
        clog.logger.info("%s %s: %s" % (getBaseC(mi, ts), heartbeatTickString, "*** no pending tasks ***"))
    return ""


# --------------------------------------------------------------------------
@task()
def TASK_displayModelCounts():
    mi = clog.dumpMethodInfo()
    ts = time.time()

    users_poi               = muser.objects.filter(ppoi=True).count()
    users_notPoi            = muser.objects.filter(ppoi=False).count()

    comments_usersAdded     = mcomment.objects.filter(puseradded=True).count()
    comments_notUsersAdded  = mcomment.objects.filter(puseradded=False).count()

    subreddits_poi          = msubreddit.objects.filter(ppoi=True).count()
    subreddits_notPoi       = msubreddit.objects.filter(ppoi=False).count()

    threads_forestGot       = mthread.objects.filter(pforestgot=True).count()
    threads_notForestGot    = mthread.objects.filter(pforestgot=False).count()

    clog.logger.info("%s %s"    % (getBaseC(mi, ts), getLine()))
    clog.logger.info("%s * %-21s %8d *" % (getBaseC(mi, ts), "Users  poi",              users_poi))
    clog.logger.info("%s * %-21s %8d *" % (getBaseC(mi, ts), "Users !poi",              users_notPoi))
    clog.logger.info("%s * %-21s %8d *" % (getBaseC(mi, ts), "Comments  users added",   comments_usersAdded))
    clog.logger.info("%s * %-21s %8d *" % (getBaseC(mi, ts), "Comments !users added",   comments_notUsersAdded))
    clog.logger.info("%s * %-21s %8d *" % (getBaseC(mi, ts), "Subreddits  poi",         subreddits_poi))
    clog.logger.info("%s * %-21s %8d *" % (getBaseC(mi, ts), "Subreddits !poi",         subreddits_notPoi))
    clog.logger.info("%s * %-21s %8d *" % (getBaseC(mi, ts), "Threads  forestGot",      threads_forestGot))
    clog.logger.info("%s * %-21s %8d *" % (getBaseC(mi, ts), "Threads !forestGot",      threads_notForestGot))
    clog.logger.info("%s %s"    % (getBaseC(mi, ts), getLine()))




