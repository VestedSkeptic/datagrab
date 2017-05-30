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
def TASK_generateModelCountData():
    mi = clog.dumpMethodInfo()

    users_poi_u             = muser.objects.filter(ppoi=True).filter(precentlyupdated=True).count()
    users_poi_nu            = muser.objects.filter(ppoi=True).filter(precentlyupdated=False).count()
    users_notPoi            = muser.objects.filter(ppoi=False).count()

    comments_usersAdded     = mcomment.objects.filter(puseradded=True).count()
    comments_notUsersAdded  = mcomment.objects.filter(puseradded=False).count()

    subreddits_poi_u        = msubreddit.objects.filter(ppoi=True).filter(precentlyupdated=True).count()
    subreddits_poi_nu       = msubreddit.objects.filter(ppoi=True).filter(precentlyupdated=False).count()
    subreddits_notPoi       = msubreddit.objects.filter(ppoi=False).count()

    threads_forestGot       = mthread.objects.filter(pforestgot=True).count()
    threads_notForestGot    = mthread.objects.filter(pforestgot=False).count()

    listOfModelCountStrings = []

    listOfModelCountStrings.append("%-30s %8d" % ("Users  poi  updated",         users_poi_u))
    listOfModelCountStrings.append("%-30s %8d" % ("Users  poi !updated",         users_poi_nu))
    listOfModelCountStrings.append("%-30s %8d" % ("Users !poi",                  users_notPoi))
    listOfModelCountStrings.append("%-30s %8d" % ("Comments  users added",       comments_usersAdded))
    listOfModelCountStrings.append("%-30s %8d" % ("Comments !users added",       comments_notUsersAdded))
    listOfModelCountStrings.append("%-30s %8d" % ("Subreddits  poi  updated",    subreddits_poi_u))
    listOfModelCountStrings.append("%-30s %8d" % ("Subreddits  poi !updated",    subreddits_poi_nu))
    listOfModelCountStrings.append("%-30s %8d" % ("Subreddits !poi",             subreddits_notPoi))
    listOfModelCountStrings.append("%-30s %8d" % ("Threads  forestGot",          threads_forestGot))
    listOfModelCountStrings.append("%-30s %8d" % ("Threads !forestGot",          threads_notForestGot))

    return listOfModelCountStrings

# --------------------------------------------------------------------------
@task()
def TASK_displayModelCounts():
    mi = clog.dumpMethodInfo()
    ts = time.time()

    listOfModelCountStrings = TASK_generateModelCountData()

    clog.logger.info("%s %s"    % (getBaseC(mi, ts), getLine()))
    for line in listOfModelCountStrings:
        # clog.logger.info("%s * %s *" % (getBaseC(mi, ts), line))
        clog.logger.info("%s   %s  " % (getBaseC(mi, ts), line))
    clog.logger.info("%s %s"    % (getBaseC(mi, ts), getLine()))
    return
