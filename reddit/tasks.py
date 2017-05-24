from celery import task
from datagrab.celery import app as celery_app               # for beat tasks
from celery.task.control import inspect                     # for ispectTasks
from celery.schedules import crontab                        # for crontab periodic tasks
from celery import current_task
from django.core.exceptions import ObjectDoesNotExist
import time
from .config import clog
from .models import mcomment
from .models import msubreddit
from .models import mthread
from .models import muser
import pprint

# --------------------------------------------------------------------------
def getTaskId():
    return current_task.request.id[:8]

# --------------------------------------------------------------------------
def getTaskP():
    return 'P'
    # return 'Processing'

# --------------------------------------------------------------------------
def getTaskC():
    return 'C'
    # return 'Completed '

# --------------------------------------------------------------------------
def getMI(mi):
    rv = mi[:-2]
    return rv.ljust(35,' ')
    # max length of task name plus trailing paranthesis is 35

# --------------------------------------------------------------------------
def getTimeDif(ts):
    td = round(time.time()-ts, 0)
    print(td)
    return '[' + str(int(td)) + ']'

# --------------------------------------------------------------------------
def getBaseP(mi):
    return "%s: %s %s:" % (getTaskId(), getMI(mi), getTaskP())

# --------------------------------------------------------------------------
def getBaseC(mi, ts):
    return "%s: %s %s: %s:" % (getTaskId(), getMI(mi), getTaskC(), getTimeDif(ts))

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
@task()
def TASK_testLogLevels():
    mi = clog.dumpMethodInfo()
    ts = time.time()

    clog.logger.critical("%s %s" % (getBaseC(mi, ts), 'critical'))
    clog.logger.error   ("%s %s" % (getBaseC(mi, ts), 'error'))
    clog.logger.warning ("%s %s" % (getBaseC(mi, ts), 'warning'))
    clog.logger.info    ("%s %s" % (getBaseC(mi, ts), 'info'))
    clog.logger.debug   ("%s %s" % (getBaseC(mi, ts), 'debug'))
    clog.logger.trace   ("%s %s" % (getBaseC(mi, ts), 'trace'))
    return ""

# --------------------------------------------------------------------------
heartbeatTickString = "TICK"
@task()
def TASK_inspectTaskQueue():
    mi = clog.dumpMethodInfo()
    ts = time.time()

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
    if heartbeatTickString == 'TICK': heartbeatTickString = 'tock'
    else:                             heartbeatTickString = 'TICK'

    if scheduledCount or activeCount or reservedCount:
        clog.logger.info("%s %s: %d active, %d scheduled, %d reserved" % (getBaseC(mi, ts), heartbeatTickString, activeCount, scheduledCount, reservedCount))
    else:
        clog.logger.info("%s %s: %s" % (getBaseC(mi, ts), heartbeatTickString, "*** no pending tasks ***"))
    return ""

# --------------------------------------------------------------------------
@task()
def TASK_testForDuplicateUsers():
    mi = clog.dumpMethodInfo()
    ts = time.time()

    clog.logger.info("%s" % (getBaseP(mi)))

    duplicateUsers = {}
    qs = muser.objects.all()
    for i_muser in qs:
        qs2 = muser.objects.filter(name=i_muser.name)

    itemsFound = qs2.count()
    if itemsFound != 1:
        duplicateUsers[i_muser.name] = 1

    if len(duplicateUsers) >= 1: clog.logger.info("%s: WARNING: %d duplicate users" % (getBaseC(mi, ts), len(duplicateUsers)))
    else:                        clog.logger.info("%s: no duplicate users found" %    (getBaseC(mi, ts)))
    return ""

# --------------------------------------------------------------------------
@task()
def TASK_updateUsersForAllComments(numberToProcess):
    mi = clog.dumpMethodInfo()
    ts = time.time()

    # create PRAW prawReddit instance
    prawReddit = mcomment.getPrawRedditInstance()
    countUsersAdded = 0

    qs = mcomment.objects.filter(puseradded=False)
    clog.logger.info("%s %d comments pending" % (getBaseP(mi),  qs.count()))
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

    clog.logger.info("%s %d comments pending, %d users added" % (getBaseC(mi, ts),   qs.count(), countUsersAdded))
    return ""

# --------------------------------------------------------------------------
@task()
def TASK_updateCommentsForAllUsers():
    mi = clog.dumpMethodInfo()
    ts = time.time()

    clog.logger.info("%s" % (getBaseP(mi)))
    qs = muser.objects.filter(ppoi=True)
    countOfTasksSpawned = 0
    for i_muser in qs:
        TASK_updateCommentsForUser.delay(i_muser.name)
        countOfTasksSpawned += 1

    clog.logger.info("%s: %d tasks spawned" % (getBaseC(mi, ts), countOfTasksSpawned))
    return ""

# --------------------------------------------------------------------------
@task()
def TASK_updateCommentsForUser(username):
    mi = clog.dumpMethodInfo()
    ts = time.time()

    try:
        i_muser = muser.objects.get(name=username)
        clog.logger.info("%s %s" % (getBaseP(mi), username))

        prawReddit = i_muser.getPrawRedditInstance()

        params={};
        params['before'] = i_muser.getBestCommentBeforeValue(prawReddit)
        # clog.logger.info("before = %s" % (params['before']))

        # iterate through submissions saving them
        countNew = 0
        countOldChanged = 0
        countOldUnchanged = 0
        try:
            for prawComment in prawReddit.redditor(i_muser.name).comments.new(limit=None, params=params):
                i_mcomment = mcomment.objects.addOrUpdate(i_muser.name, prawComment)
                if i_mcomment.addOrUpdateTempField == "new":            countNew += 1
                if i_mcomment.addOrUpdateTempField == "oldUnchanged":   countOldUnchanged += 1
                if i_mcomment.addOrUpdateTempField == "oldChanged":     countOldChanged += 1
                i_mcomment.puseradded = True
                i_mcomment.save()
        except praw.exceptions.APIException as e:
            clog.logger.info("%s: %s PRAW_APIException: error_type = %s, message = %s" % (getBaseC(mi, ts), username, e.error_type, e.message))
        clog.logger.info("%s: %s, %d new, %d old, %d oldChanged" % (getBaseC(mi, ts), username, countNew, countOldUnchanged, countOldChanged))
    except ObjectDoesNotExist:
        clog.logger.info("%s: %s, %s" % (getBaseC(mi, ts), username, "ERROR does not exist"))
    return ""

# --------------------------------------------------------------------------
@task()
def TASK_updateThreadsForSubreddit(subredditName):
    mi = clog.dumpMethodInfo()
    ts = time.time()

    try:
        i_msubreddit = msubreddit.objects.get(name=subredditName)
        clog.logger.info("%s %s" % (getBaseP(mi), subredditName))

        prawReddit = i_msubreddit.getPrawRedditInstance()

        params={};
        params['before'] = i_msubreddit.getThreadsBestBeforeValue(prawReddit)
        # clog.logger.info("before = %s" % (params['before']))

        countNew = 0
        countOldUnchanged = 0
        countOldChanged = 0
        try:
            for prawThread in prawReddit.subreddit(i_msubreddit.name).new(limit=None, params=params):
                i_mthread = mthread.objects.addOrUpdate(i_msubreddit, prawThread)
                if i_mthread.addOrUpdateTempField == "new":             countNew += 1
                if i_mthread.addOrUpdateTempField == "oldUnchanged":    countOldUnchanged += 1
                if i_mthread.addOrUpdateTempField == "oldChanged":      countOldChanged += 1
        except praw.exceptions.APIException as e:
            clog.logger.info("%s %s PRAW_APIException: error_type = %s, message = %s" % (getBaseC(mi, ts), subredditName, e.error_type, e.message))
        clog.logger.info("%s %s, %d new, %d old, %d oldChanged" % (getBaseC(mi, ts), subredditName, countNew, countOldUnchanged, countOldChanged))
    except ObjectDoesNotExist:
        clog.logger.info("%s %s, %s" % (getBaseC(mi, ts), subredditName, "ERROR does not exist"))
    return ""

# --------------------------------------------------------------------------
@task()
def TASK_updateThreadsByCommentForest(numberToProcess):
    mi = clog.dumpMethodInfo()
    ts = time.time()

    # create PRAW prawReddit instance
    prawReddit = mcomment.getPrawRedditInstance()
    countCommentsAdded = 0

    qs = mthread.objects.filter(pdeleted=False, pforestgot=False).order_by("-rcreated")
    clog.logger.info("%s %d threads pending, processing %d" % (getBaseP(mi),  qs.count(), numberToProcess))

    countNew = 0
    countOldChanged = 0
    countOldUnchanged = 0
    countDeleted = 0

    for i_mthread in qs:
        try:
            params={};
            # params['before'] = i_mthread.getBestCommentBeforeValue(????)

            prawSubmissionObject = prawReddit.submission(id=i_mthread.fullname[3:])
            prawSubmissionObject.comment_sort = "new"

            # prawSubmissionObject.comments.replace_more(limit=None)
            prawSubmissionObject.comments.replace_more(limit=16)

            for prawComment in prawSubmissionObject.comments.list():
                if prawComment.author == None:
                    countDeleted += 1
                else:
                    i_mcomment = mcomment.objects.addOrUpdate(prawComment.author.name, prawComment)
                    if i_mcomment.addOrUpdateTempField == "new":            countNew += 1
                    if i_mcomment.addOrUpdateTempField == "oldUnchanged":   countOldUnchanged += 1
                    if i_mcomment.addOrUpdateTempField == "oldChanged":     countOldChanged += 1
        except praw.exceptions.APIException as e:
            clog.logger.info("%s %s PRAW_APIException: error_type = %s, message = %s" % (getBaseP(mi), username, e.error_type, e.message))

        i_mthread.pforestgot = True
        i_mthread.pcount += countNew
        i_mthread.save()

        numberToProcess -= 1
        if numberToProcess <= 0:
            break

    clog.logger.info("%s %d new, %d old, %d oldChanged, %d deleted" % (getBaseC(mi, ts), countNew, countOldUnchanged, countOldChanged, countDeleted))
    return ""

# --------------------------------------------------------------------------
# can add expires parameter (in seconds) so task times out if it hasn't occurred
# in this time period.
# Ex: sender.add_periodic_task(60.0,      TASK_template.s(), expires=10)
@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(  5.0,      TASK_testLogLevels.s())
    # sender.add_periodic_task(  5.0,      TASK_template.s())
    # sender.add_periodic_task( 300.0,    TASK_inspectTaskQueue.s())

    sender.add_periodic_task(  90.0,    TASK_updateThreadsByCommentForest.s(20))
    sender.add_periodic_task( 300.0,    TASK_updateUsersForAllComments.s(100))
    sender.add_periodic_task( 600.0,    TASK_updateThreadsForSubreddit.s('politics'))
    sender.add_periodic_task( 750.0,    TASK_updateThreadsForSubreddit.s('The_Donald'))
    sender.add_periodic_task( 900.0,    TASK_updateThreadsForSubreddit.s('AskThe_Donald'))
    sender.add_periodic_task(1200.0,    TASK_updateThreadsForSubreddit.s('Le_Pen'))
    sender.add_periodic_task(1200.0,    TASK_updateThreadsForSubreddit.s('AgainstHateSubreddits'))
    sender.add_periodic_task(1200.0,    TASK_updateThreadsForSubreddit.s('TheNewRight'))
    sender.add_periodic_task(7200.0,    TASK_updateThreadsForSubreddit.s('Molw'))
    sender.add_periodic_task(2400.0,    TASK_updateCommentsForAllUsers.s())
    sender.add_periodic_task(7200.0,    TASK_testForDuplicateUsers.s())

    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )










