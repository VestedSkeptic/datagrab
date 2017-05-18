from celery import task
from .config import clog
from .blue import bthread
from .models import msubreddit
from django.core.exceptions import ObjectDoesNotExist

# --------------------------------------------------------------------------
@task()
def red(x, y):
    return x + y

# --------------------------------------------------------------------------
@task()
def add(x, y):
    return x + y

# --------------------------------------------------------------------------
@task()
def orange(x, y):
    return x + y


# --------------------------------------------------------------------------
# def getMoreThreadsForSubredditName(subredditName):
@task()
def black(subredditName):
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)

    clog.logger.info("001")

    try:
        i_msubreddit = msubreddit.objects.get(name=subredditName)
        bthread.getMoreThreadsForSubredditInstance(i_msubreddit=i_msubreddit)
        return "yes"
    except ObjectDoesNotExist:
        # clog.logger.info("%s: subreddit %s does not exist" % (mi, subredditName))
        return "no"



#
# # --------------------------------------------------------------------------
# def initializeCLogger():
#     global clog


#### SCHEDULE SHELL ####
# python manage.py shell
# > from reddit.config import initializeCLogger
# > initializeCLogger()
# > from reddit.tasks import black
# > black.delay("Molw")

#### WORKER SHELL ####
# Change in code requires restart of worker
# python manage.py celery worker --loglevel=info



















