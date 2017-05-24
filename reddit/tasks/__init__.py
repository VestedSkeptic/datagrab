from datagrab.celery import app as celery_app               # for beat tasks
from celery.schedules import crontab                        # for crontab periodic tasks

from .tmisc import TASK_template, TASK_inspectTaskQueue
from .treddit import TASK_updateUsersForAllComments, TASK_updateCommentsForAllUsers, TASK_updateCommentsForUser, TASK_updateThreadsForSubreddit, TASK_updateThreadsByCommentForest
from .ttest import TASK_testLogLevels, TASK_testForDuplicateUsers, TASK_testForDuplicateComments

# --------------------------------------------------------------------------
# can add expires parameter (in seconds) so task times out if it hasn't occurred
# in this time period.
# Ex: sender.add_periodic_task(60.0,      TASK_template.s(), expires=10)
@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(  5.0,      TASK_testLogLevels.s())
    sender.add_periodic_task(  5.0,      TASK_template.s())
    # sender.add_periodic_task( 300.0,    TASK_inspectTaskQueue.s())
    sender.add_periodic_task( 5.0,    TASK_inspectTaskQueue.s())

    # sender.add_periodic_task(  90.0,    TASK_updateThreadsByCommentForest.s(25))
    # sender.add_periodic_task( 300.0,    TASK_updateUsersForAllComments.s(100))
    # sender.add_periodic_task( 800.0,    TASK_updateThreadsForSubreddit.s('politics'))
    # sender.add_periodic_task( 800.0,    TASK_updateThreadsForSubreddit.s('The_Donald'))
    # sender.add_periodic_task(1300.0,    TASK_updateThreadsForSubreddit.s('AskThe_Donald'))
    # sender.add_periodic_task(1400.0,    TASK_updateThreadsForSubreddit.s('Le_Pen'))
    # sender.add_periodic_task(1400.0,    TASK_updateThreadsForSubreddit.s('AgainstHateSubreddits'))
    # sender.add_periodic_task(1400.0,    TASK_updateThreadsForSubreddit.s('TheNewRight'))
    # sender.add_periodic_task(7200.0,    TASK_updateThreadsForSubreddit.s('Molw'))
    # sender.add_periodic_task(7200.0,    TASK_updateCommentsForAllUsers.s())
    # sender.add_periodic_task(7200.0,    TASK_testForDuplicateUsers.s())
    # sender.add_periodic_task(7200.0,    TASK_testForDuplicateComments.s())

    # TASK_testForDuplicateUsers.delay()
    # TASK_testForDuplicateComments.delay()

    pass

    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )





