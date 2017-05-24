from celery import task
import time
from ..config import clog
from ..models import mcomment
from ..models import msubreddit
from ..models import mthread
from ..models import muser
from .tbase import getBaseP, getBaseC
# import pprint

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

    if len(duplicateUsers) >= 1: clog.logger.info("%s WARNING: %d duplicate users" % (getBaseC(mi, ts), len(duplicateUsers)))
    else:                        clog.logger.info("%s no duplicate users found" %    (getBaseC(mi, ts)))
    return ""

# --------------------------------------------------------------------------
@task()
def TASK_testForDuplicateComments():
    mi = clog.dumpMethodInfo()
    ts = time.time()

    clog.logger.info("%s" % (getBaseP(mi)))

    duplicateComments = {}
    qs = mcomment.objects.all()
    for i_mcomment in qs:
        qs2 = mcomment.objects.filter(username=i_mcomment.username, name=i_mcomment.name, thread=i_mcomment.thread, subreddit=i_mcomment.subreddit)

    itemsFound = qs2.count()
    if itemsFound != 1:
        duplicateComments[i_mcomment.name] = 1

    if len(duplicateComments) >= 1: clog.logger.info("%s: WARNING: %d duplicate comments" % (getBaseC(mi, ts), len(duplicateComments)))
    else:                           clog.logger.info("%s: no duplicate comments found" %    (getBaseC(mi, ts)))
    return ""











