from datagrab.celery import app as celery_app               # for beat tasks
from celery.schedules import crontab                        # for crontab periodic tasks

from .tmisc import TASK_template, TASK_inspectTaskQueue
from .treddit import TASK_updateUsersForAllComments, TASK_updateCommentsForAllUsers, TASK_updateCommentsForUser, TASK_updateThreadsForSubreddit, TASK_updateThreadsByCommentForest
from .ttest import TASK_testLogLevels, TASK_testForDuplicateUsers, TASK_testForDuplicateComments



# CONST_MINUTE    = 60
# CONST_HOUR      = 3600



# --------------------------------------------------------------------------
# can add expires parameter (in seconds)
# Ex: sender.add_periodic_task(60.0,      TASK_template.s(), expires=10)
@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(  5.0,      TASK_testLogLevels.s())
    # sender.add_periodic_task(  5.0,      TASK_template.s())
    sender.add_periodic_task(  60.0,    TASK_inspectTaskQueue.s(), expires=120)

    # sender.add_periodic_task(  90.0,    TASK_updateThreadsByCommentForest.s(25))
    # sender.add_periodic_task( 300.0,    TASK_updateUsersForAllComments.s(100))
    # sender.add_periodic_task(1200.0,    TASK_updateThreadsForSubreddit.s('politics'))
    # sender.add_periodic_task(1200.0,    TASK_updateThreadsForSubreddit.s('The_Donald'))
    # sender.add_periodic_task(1210.0,    TASK_updateThreadsForSubreddit.s('AskThe_Donald'))
    # sender.add_periodic_task(1400.0,    TASK_updateThreadsForSubreddit.s('Le_Pen'))
    # sender.add_periodic_task(1400.0,    TASK_updateThreadsForSubreddit.s('AgainstHateSubreddits'))
    # sender.add_periodic_task(1400.0,    TASK_updateThreadsForSubreddit.s('TheNewRight'))
    # sender.add_periodic_task(7200.0,    TASK_updateThreadsForSubreddit.s('Molw'))
    # sender.add_periodic_task(7200.0,    TASK_updateCommentsForAllUsers.s())
    # sender.add_periodic_task(7200.0,    TASK_testForDuplicateUsers.s())
    # sender.add_periodic_task(7200.0,    TASK_testForDuplicateComments.s())

    pass



# --------------------------------------------------------------------------
@celery_app.on_after_finalize.connect
def launch_tasks_on_startup(sender, **kwargs):
    TASK_updateThreadsByCommentForest.delay(1000)
    # TASK_updateUsersForAllComments.delay(100)
    # TASK_updateThreadsForSubreddit.delay('politics')
    # TASK_updateThreadsForSubreddit.delay('The_Donald')
    # TASK_updateThreadsForSubreddit.delay('AskThe_Donald')
    # TASK_updateThreadsForSubreddit.delay('Le_Pen')
    # TASK_updateThreadsForSubreddit.delay('AgainstHateSubreddits')
    # TASK_updateThreadsForSubreddit.delay('TheNewRight')
    # TASK_updateThreadsForSubreddit.delay('Molw')
    # TASK_updateCommentsForAllUsers.delay()
    # TASK_testForDuplicateUsers.delay()
    # TASK_testForDuplicateComments.delay()
    pass




# --------------------------------------------------------------------------
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )



    # task.delay(arg1,arg2)       #will be async
    # task.delay(arg1,arg2).get() #will be sync
    # task.delay(arg1,arg2).get() #will be sync
