# from datagrab.celery import app as celery_app               # for beat tasks
from celery import current_task
import time


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
    return rv.ljust(35,' ')  # max length of task name plus trailing paranthesis is 35

# --------------------------------------------------------------------------
def getTimeDif(ts):
    td = round(time.time()-ts, 0)
    return '[' + str(int(td)) + ']'

# --------------------------------------------------------------------------
def getBaseP(mi):
    return "%s: %s %s:" % (getTaskId(), getMI(mi), getTaskP())

# --------------------------------------------------------------------------
def getBaseC(mi, ts):
    return "%s: %s %s: %s:" % (getTaskId(), getMI(mi), getTaskC(), getTimeDif(ts))

# --------------------------------------------------------------------------
def getLine():
    return "**********************************"








