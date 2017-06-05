from datagrab.celery import app as celery_app               # for beat tasks
from celery.schedules import crontab                        # for crontab periodic tasks
from .tmisc import TASK_template, TASK_inspectTaskQueue, TASK_displayModelCounts
from .treddit import TASK_updateUsersForAllComments, TASK_updateCommentsForAllUsers, TASK_updateCommentsForUser, TASK_updateThreadsForAllSubreddits, TASK_updateThreadCommentsByForest
from .ttest import TASK_testLogLevels, TASK_testForDuplicateUsers, TASK_testForDuplicateComments

CONST_SECONDS_05            = 5

CONST_MINUTES_02            = 120
CONST_MINUTES_05            = 300
CONST_MINUTES_10            = 600
CONST_MINUTES_15            = 900
CONST_MINUTES_20            = 1200
CONST_MINUTES_30            = 1800

CONST_HOURS___01            = 3600
CONST_HOURS___02            = CONST_HOURS___01*2
CONST_HOURS___03            = CONST_HOURS___01*3
CONST_HOURS___04            = CONST_HOURS___01*4
CONST_HOURS___05            = CONST_HOURS___01*5
CONST_HOURS___06            = CONST_HOURS___01*6
CONST_HOURS___12            = CONST_HOURS___01*12

# --------------------------------------------------------------------------
# can add expires parameter (in seconds)
# Ex: sender.add_periodic_task(60.0,      TASK_template.s(), expires=10)
@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(CONST_SECONDS_05,  TASK_testLogLevels.s())
    # sender.add_periodic_task(CONST_SECONDS_05,  TASK_template.s())

    sender.add_periodic_task(CONST_MINUTES_02,  TASK_inspectTaskQueue.s(),                      expires=CONST_MINUTES_02-10)
    sender.add_periodic_task(CONST_MINUTES_05,  TASK_updateThreadsForAllSubreddits.s(2, 0),     expires=CONST_MINUTES_05-10)
    sender.add_periodic_task(CONST_MINUTES_30,  TASK_updateThreadsForAllSubreddits.s(2, 1),     expires=CONST_MINUTES_30-10)
    sender.add_periodic_task(CONST_HOURS___04,  TASK_updateThreadsForAllSubreddits.s(2, 2),     expires=CONST_HOURS___04-10)

    sender.add_periodic_task(CONST_MINUTES_05,  TASK_updateCommentsForAllUsers.s(10, 0),        expires=CONST_MINUTES_05-10)
    sender.add_periodic_task(CONST_HOURS___02,  TASK_updateCommentsForAllUsers.s(10, 1),        expires=CONST_HOURS___02-10)
    sender.add_periodic_task(CONST_HOURS___06,  TASK_updateCommentsForAllUsers.s(10, 2),        expires=CONST_HOURS___06-10)

    sender.add_periodic_task(CONST_MINUTES_10,  TASK_displayModelCounts.s(),                    expires=CONST_MINUTES_10-10)

    sender.add_periodic_task(CONST_MINUTES_02,  TASK_updateThreadCommentsByForest.s(30),        expires=CONST_MINUTES_02-10)
    sender.add_periodic_task(CONST_MINUTES_05,  TASK_updateUsersForAllComments.s(100),          expires=CONST_MINUTES_05-10)
    sender.add_periodic_task(CONST_HOURS___02,  TASK_testForDuplicateUsers.s(),                 expires=CONST_HOURS___02-10)
    sender.add_periodic_task(CONST_HOURS___02,  TASK_testForDuplicateComments.s(),              expires=CONST_HOURS___02-10)

    pass

# --------------------------------------------------------------------------
@celery_app.on_after_finalize.connect
def launch_tasks_on_startup(sender, **kwargs):
    # TASK_inspectTaskQueue.delay()
    # TASK_displayModelCounts.delay()

    # TASK_updateThreadsForAllSubreddits.delay(1, 0)
    # TASK_updateThreadsForAllSubreddits.delay(1, 1)
    # TASK_updateThreadsForAllSubreddits.delay(1, 2)
    # TASK_updateCommentsForAllUsers.delay(1, 0)
    # TASK_updateCommentsForAllUsers.delay(1, 1)
    # TASK_updateCommentsForAllUsers.delay(1, 2)

    # TASK_updateCommentsForAllUsers.delay(1, True)

    # TASK_updateThreadCommentsByForest.delay(30)
    # TASK_updateUsersForAllComments.delay(100)
    #
    # # TASK_testForDuplicateUsers.delay()
    # # TASK_testForDuplicateComments.delay()

    pass




# --------------------------------------------------------------------------
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )



    # task.delay(arg1,arg2)       #will be async
    # task.delay(arg1,arg2).get() #will be sync
    # task.delay(arg1,arg2).get() #will be sync
