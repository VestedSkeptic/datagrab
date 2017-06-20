from celery import task
import time
from django.db.models import Count
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
def TASK_testForDuplicateComments():
    mi = clog.dumpMethodInfo()
    ts = time.time()
    clog.logger.info("%s" % (getBaseP(mi)))

    qs = mcomment.objects.values('username','name','thread','subreddit').annotate(num_count=Count('name')).filter(num_count__gt=1)
    if qs.count() > 0:
        clog.logger.info("%s WARNING: at least %d duplicate comments" % (getBaseC(mi, ts), qs.count()))
        for i_mac in qs:
            value = int(i_mac['num_count'])
            while value > 1:
                clog.logger.info("%s WARNING: deleting %s, thread %s, subreddit %s, username %s" % (getBaseC(mi, ts), i_mac['name'], i_mac['thread'], i_mac['subreddit'], i_mac['username']))
                qs2 = mcomment.objects.filter(username=i_mac['username'], name=i_mac['name'], thread=i_mac['thread'], subreddit=i_mac['subreddit'])
                qs2.delete()
                value -= 1
    else:
        clog.logger.info("%s no duplicate comments found" %    (getBaseC(mi, ts)))
    return ""

# --------------------------------------------------------------------------
@task()
def TASK_testForDuplicateThreads():
    mi = clog.dumpMethodInfo()
    ts = time.time()
    clog.logger.info("%s" % (getBaseP(mi)))

    qs = mthread.objects.values('fullname').annotate(num_count=Count('fullname')).filter(num_count__gt=1)
    if qs.count() > 0:
        clog.logger.info("%s WARNING: at least %d duplicate threads" % (getBaseC(mi, ts), qs.count()))
        for i_mac in qs:
            value = int(i_mac['num_count'])
            while value > 1:
                clog.logger.info("%s WARNING: deleting %s" % (getBaseC(mi, ts), i_mac['fullname']))
                qs2 = mthread.objects.filter(fullname=i_mac['fullname'])
                qs2.delete()
                value -= 1
    else:
        clog.logger.info("%s no duplicate threads found" %    (getBaseC(mi, ts)))
    return ""

# --------------------------------------------------------------------------
@task()
def TASK_testForDuplicateUsers():
    mi = clog.dumpMethodInfo()
    ts = time.time()
    clog.logger.info("%s" % (getBaseP(mi)))

    qs = muser.objects.values('name').annotate(num_count=Count('name')).filter(num_count__gt=1)
    if qs.count() > 0:
        clog.logger.info("%s WARNING: at least %d duplicate users" % (getBaseC(mi, ts), qs.count()))
        for i_mac in qs:
            value = int(i_mac['num_count'])
            while value > 1:
                clog.logger.info("%s WARNING: deleting %s" % (getBaseC(mi, ts), i_mac['name']))
                qs2 = muser.objects.filter(name=i_mac['name']).order_by('-pcommentsupdatetimestamp')
                qs2.delete()
                value -= 1
    else:
        clog.logger.info("%s no duplicate users found" %    (getBaseC(mi, ts)))
    return ""




