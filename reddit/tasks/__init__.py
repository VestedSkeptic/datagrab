from datagrab.celery import app as celery_app               # for beat tasks
from celery.schedules import crontab                        # for crontab periodic tasks

from .tmisc import TASK_template, TASK_inspectTaskQueue, TASK_displayModelCounts
from .treddit import TASK_updateUsersForAllComments, TASK_updateCommentsForAllUsers, TASK_updateCommentsForUser, TASK_updateThreadsForSubreddit, TASK_updateThreadCommentsByForest
from .ttest import TASK_testLogLevels, TASK_testForDuplicateUsers, TASK_testForDuplicateComments

# --------------------------------------------------------------------------
# can add expires parameter (in seconds)
# Ex: sender.add_periodic_task(60.0,      TASK_template.s(), expires=10)
@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(  5.0,      TASK_testLogLevels.s())
    # sender.add_periodic_task(  5.0,      TASK_template.s())

    sender.add_periodic_task(  60.0,    TASK_inspectTaskQueue.s(), expires=120)
    sender.add_periodic_task( 120.0,    TASK_updateCommentsForAllUsers.s(2, False))

    # # sender.add_periodic_task( 120.0,    TASK_updateThreadCommentsByForest.s(30),                      expires=160)
    # # sender.add_periodic_task( 300.0,    TASK_updateUsersForAllComments.s(100),                        expires=400)
    # # # sender.add_periodic_task(1800.0,    TASK_updateThreadsForSubreddit.s('politics'),                 expires=2200)
    # # # sender.add_periodic_task(1805.0,    TASK_updateThreadsForSubreddit.s('The_Donald'),               expires=2205)
    # # # sender.add_periodic_task(1810.0,    TASK_updateThreadsForSubreddit.s('AskThe_Donald'),            expires=2210)
    # # # sender.add_periodic_task(3600.0,    TASK_updateThreadsForSubreddit.s('Le_Pen'))
    # # # sender.add_periodic_task(3605.0,    TASK_updateThreadsForSubreddit.s('AgainstHateSubreddits'))
    # # # sender.add_periodic_task(3610.0,    TASK_updateThreadsForSubreddit.s('TheNewRight'))
    # # # sender.add_periodic_task(3610.0,    TASK_updateThreadsForSubreddit.s('PoliticalDiscussion'))
    # # # sender.add_periodic_task(3610.0,    TASK_updateThreadsForSubreddit.s('NeutralPolitics'))
    # # # sender.add_periodic_task(3610.0,    TASK_updateThreadsForSubreddit.s('Keep_Track'))
    # # # sender.add_periodic_task(7100.0,    TASK_updateThreadsForSubreddit.s('Molw'))
    # # sender.add_periodic_task(8000.0,    TASK_testForDuplicateUsers.s())
    # # sender.add_periodic_task(9000.0,    TASK_testForDuplicateComments.s())
    # # sender.add_periodic_task(3599.0,    TASK_displayModelCounts.s())

    pass

# --------------------------------------------------------------------------
@celery_app.on_after_finalize.connect
def launch_tasks_on_startup(sender, **kwargs):
    TASK_displayModelCounts.delay()
    TASK_updateCommentsForAllUsers.delay(1, True)


    # TASK_updateThreadsForSubreddit.delay('politics')
    # TASK_updateThreadsForSubreddit.delay('The_Donald')
    # TASK_updateThreadsForSubreddit.delay('AskThe_Donald')
    # TASK_updateThreadsForSubreddit.delay('Le_Pen')
    # TASK_updateThreadsForSubreddit.delay('AgainstHateSubreddits')
    # TASK_updateThreadsForSubreddit.delay('TheNewRight')
    # TASK_updateThreadsForSubreddit.delay('Molw')
    # TASK_updateThreadsForSubreddit.delay('PoliticalDiscussion')
    # TASK_updateThreadsForSubreddit.delay('NeutralPolitics')
    # TASK_updateThreadsForSubreddit.delay('Keep_Track')

    # TASK_updateThreadCommentsByForest.delay(200)

    # TASK_updateUsersForAllComments.delay(100)
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
