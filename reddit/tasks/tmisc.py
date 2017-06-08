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

    users_poi               = muser.objects.filter(ppoi=True).count()
    users_notPoi            = muser.objects.filter(ppoi=False).count()

    users_poi_pri_0         = muser.objects.filter(ppoi=True).filter(pprioritylevel=0).count()
    users_poi_pri_1         = muser.objects.filter(ppoi=True).filter(pprioritylevel=1).count()
    users_poi_pri_2         = muser.objects.filter(ppoi=True).filter(pprioritylevel=2).count()

    comments_usersAdded     = mcomment.objects.filter(puseradded=True).count()
    comments_notUsersAdded  = mcomment.objects.filter(puseradded=False).count()

    subreddits_poi          = msubreddit.objects.filter(ppoi=True).count()
    subreddits_notPoi       = msubreddit.objects.filter(ppoi=False).count()

    subreddits_poi_pri_0    = msubreddit.objects.filter(ppoi=True).filter(pprioritylevel=0).count()
    subreddits_poi_pri_1    = msubreddit.objects.filter(ppoi=True).filter(pprioritylevel=1).count()
    subreddits_poi_pri_2    = msubreddit.objects.filter(ppoi=True).filter(pprioritylevel=2).count()

    threads_forestGot       = mthread.objects.filter(pforestgot=True).count()
    threads_notForestGot    = mthread.objects.filter(pforestgot=False).count()

    listOfModelCountStrings = []

    listOfModelCountStrings.append("%-30s %8d" % ("Users  poi",                  users_poi))
    listOfModelCountStrings.append("%-30s %8d" % ("Users !poi",                  users_notPoi))
    listOfModelCountStrings.append("%s" % ("---------------------------------------"))
    listOfModelCountStrings.append("%-30s %8d" % ("Users  poi priority 0",       users_poi_pri_0))
    listOfModelCountStrings.append("%-30s %8d" % ("Users  poi priority 1",       users_poi_pri_1))
    listOfModelCountStrings.append("%-30s %8d" % ("Users  poi priority 2",       users_poi_pri_2))
    listOfModelCountStrings.append("%s" % ("---------------------------------------"))
    listOfModelCountStrings.append("%-30s %8d" % ("Comments  users added",       comments_usersAdded))
    listOfModelCountStrings.append("%-30s %8d" % ("Comments !users added",       comments_notUsersAdded))
    listOfModelCountStrings.append("%-30s %8d" % ("Comments  total",             comments_usersAdded + comments_notUsersAdded))
    listOfModelCountStrings.append("%s" % ("---------------------------------------"))
    listOfModelCountStrings.append("%-30s %8d" % ("Subreddits  poi",             subreddits_poi))
    listOfModelCountStrings.append("%-30s %8d" % ("Subreddits !poi",             subreddits_notPoi))
    listOfModelCountStrings.append("%s" % ("---------------------------------------"))
    listOfModelCountStrings.append("%-30s %8d" % ("Subreddits  poi  priority 0", subreddits_poi_pri_0))
    listOfModelCountStrings.append("%-30s %8d" % ("Subreddits  poi  priority 1", subreddits_poi_pri_1))
    listOfModelCountStrings.append("%-30s %8d" % ("Subreddits  poi  priority 2", subreddits_poi_pri_2))
    listOfModelCountStrings.append("%s" % ("---------------------------------------"))
    listOfModelCountStrings.append("%-30s %8d" % ("Threads  forestGot",          threads_forestGot))
    listOfModelCountStrings.append("%-30s %8d" % ("Threads !forestGot",          threads_notForestGot))
    listOfModelCountStrings.append("%-30s %8d" % ("Threads  total",              threads_forestGot + threads_notForestGot))

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
