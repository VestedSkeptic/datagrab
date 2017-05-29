from datagrab.celery import app as celery_app               # for beat tasks
from celery.schedules import crontab                        # for crontab periodic tasks

from .tmisc import TASK_template, TASK_inspectTaskQueue, TASK_displayModelCounts
from .treddit import TASK_updateUsersForAllComments, TASK_updateCommentsForAllUsers, TASK_updateCommentsForUser, TASK_updateThreadsForAllSubreddits, TASK_updateThreadCommentsByForest
from .ttest import TASK_testLogLevels, TASK_testForDuplicateUsers, TASK_testForDuplicateComments

# --------------------------------------------------------------------------
# can add expires parameter (in seconds)
# Ex: sender.add_periodic_task(60.0,      TASK_template.s(), expires=10)
@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(  5.0,      TASK_testLogLevels.s())
    # sender.add_periodic_task(  5.0,      TASK_template.s())

    sender.add_periodic_task( 120.0,    TASK_inspectTaskQueue.s(), expires=120)
    sender.add_periodic_task( 600.0,    TASK_displayModelCounts.s())
    sender.add_periodic_task( 180.0,    TASK_updateCommentsForAllUsers.s(2, False),         expires=358)
    sender.add_periodic_task( 360.0,    TASK_updateThreadsForAllSubreddits.s(2, False),     expires=718)

    sender.add_periodic_task( 120.0,    TASK_updateThreadCommentsByForest.s(30),            expires=238)
    sender.add_periodic_task( 300.0,    TASK_updateUsersForAllComments.s(100),              expires=598)

    sender.add_periodic_task(3600.0,    TASK_testForDuplicateUsers.s())
    sender.add_periodic_task(3660.0,    TASK_testForDuplicateComments.s())

    pass

# --------------------------------------------------------------------------
@celery_app.on_after_finalize.connect
def launch_tasks_on_startup(sender, **kwargs):
    # TASK_inspectTaskQueue.delay()
    # TASK_displayModelCounts.delay()
    # # TASK_updateCommentsForAllUsers.delay(1, True)
    # # TASK_updateThreadsForAllSubreddits.delay(1, True)
    #
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
