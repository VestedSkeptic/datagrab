from datagrab.celery import app as celery_app               # for beat tasks
from celery.schedules import crontab                        # for crontab periodic tasks
from .tmisc import TASK_template, TASK_inspectTaskQueue, TASK_displayModelCounts
from .treddit import TASK_updateUsersForAllComments, TASK_updateCommentsForAllUsers, TASK_updateCommentsForUser, TASK_updateThreadsForAllSubreddits, TASK_updateThreadCommentsByForest
from .ttest import TASK_testLogLevels, TASK_testForDuplicateUsers, TASK_testForDuplicateComments, TASK_testForDuplicateThreads

CONST_SECONDS_05            = 5

CONST_MINUTES_01            = 60
CONST_MINUTES_02            = CONST_MINUTES_01*2
CONST_MINUTES_05            = CONST_MINUTES_01*5
CONST_MINUTES_10            = CONST_MINUTES_01*10
CONST_MINUTES_15            = CONST_MINUTES_01*15
CONST_MINUTES_20            = CONST_MINUTES_01*20
CONST_MINUTES_30            = CONST_MINUTES_01*30

CONST_HOURS___01            = CONST_MINUTES_01*60
CONST_HOURS___02            = CONST_HOURS___01*2
CONST_HOURS___03            = CONST_HOURS___01*3
CONST_HOURS___04            = CONST_HOURS___01*4
CONST_HOURS___05            = CONST_HOURS___01*5
CONST_HOURS___06            = CONST_HOURS___01*6
CONST_HOURS___07            = CONST_HOURS___01*7
CONST_HOURS___08            = CONST_HOURS___01*8
CONST_HOURS___09            = CONST_HOURS___01*9
CONST_HOURS___10            = CONST_HOURS___01*10
CONST_HOURS___11            = CONST_HOURS___01*11
CONST_HOURS___12            = CONST_HOURS___01*12

# --------------------------------------------------------------------------
# can add expires parameter (in seconds)
# Ex: sender.add_periodic_task(60.0,      TASK_template.s(), expires=10)
@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(CONST_SECONDS_05,  TASK_testLogLevels.s())
    # sender.add_periodic_task(CONST_SECONDS_05,  TASK_template.s())

    sender.add_periodic_task(CONST_MINUTES_02,  TASK_inspectTaskQueue.s(),                      expires=CONST_MINUTES_02-10)

    sender.add_periodic_task(CONST_MINUTES_15,  TASK_updateThreadsForAllSubreddits.s(20, 0),    expires=CONST_MINUTES_15-10)
    sender.add_periodic_task(CONST_HOURS___01,  TASK_updateThreadsForAllSubreddits.s(20, 1),    expires=CONST_HOURS___01-10)
    sender.add_periodic_task(CONST_HOURS___02,  TASK_updateThreadsForAllSubreddits.s(20, 2),    expires=CONST_HOURS___02-10)
    sender.add_periodic_task(CONST_HOURS___02,  TASK_updateThreadsForAllSubreddits.s(20, 3),    expires=CONST_HOURS___02-10)

    sender.add_periodic_task(CONST_HOURS___01,  TASK_updateCommentsForAllUsers.s(100, 0),       expires=CONST_HOURS___01-10)
    sender.add_periodic_task(CONST_HOURS___02,  TASK_updateCommentsForAllUsers.s(100, 1),       expires=CONST_HOURS___02-10)
    sender.add_periodic_task(CONST_HOURS___03,  TASK_updateCommentsForAllUsers.s(100, 2),       expires=CONST_HOURS___03-10)
    sender.add_periodic_task(CONST_HOURS___04,  TASK_updateCommentsForAllUsers.s(100, 3),       expires=CONST_HOURS___04-10)

    sender.add_periodic_task(CONST_MINUTES_10,  TASK_displayModelCounts.s(),                    expires=CONST_MINUTES_10-10)

    sender.add_periodic_task(CONST_MINUTES_02,  TASK_updateThreadCommentsByForest.s(30),        expires=CONST_MINUTES_02-10)
    sender.add_periodic_task(CONST_MINUTES_05,  TASK_updateUsersForAllComments.s(100),          expires=CONST_MINUTES_05-10)
    sender.add_periodic_task(CONST_HOURS___03,  TASK_testForDuplicateUsers.s(),                 expires=CONST_HOURS___03-10)
    sender.add_periodic_task(CONST_HOURS___03,  TASK_testForDuplicateComments.s(),              expires=CONST_HOURS___03-10)
    sender.add_periodic_task(CONST_HOURS___03,  TASK_testForDuplicateThreads.s(),               expires=CONST_HOURS___03-10)

    pass

# --------------------------------------------------------------------------
@celery_app.on_after_finalize.connect
def launch_tasks_on_startup(sender, **kwargs):
    # TASK_inspectTaskQueue.delay()
    # TASK_displayModelCounts.delay()

    # TASK_updateThreadCommentsByForest.delay(30)
    # TASK_updateUsersForAllComments.delay(100)
    # TASK_testForDuplicateUsers.delay()
    # TASK_testForDuplicateComments.delay()
    # TASK_testForDuplicateThreads.delay()
    # TASK_updateCommentsForAllUsers.delay(2000, -1)
    # TASK_updateThreadsForAllSubreddits.delay(51, 3)
    # TASK_updateThreadsForAllSubreddits.delay(51, 2)
    # TASK_updateThreadsForAllSubreddits.delay(51, 1)
    # TASK_updateThreadsForAllSubreddits.delay(51, 0)

    pass



# --------------------------------------------------------------------------
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )



    # task.delay(arg1,arg2)       #will be async
    # task.delay(arg1,arg2).get() #will be sync
    # task.delay(arg1,arg2).get() #will be sync
