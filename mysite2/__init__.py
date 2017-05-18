# *****************************************************************************
# Import mysite2/mysite2/celery.py
from __future__ import absolute_import, unicode_literals
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app
__all__ = ['celery_app']

# *****************************************************************************
# Update sys.path to allow importing python files from libPython directory
import sys
sys.path.insert(0, "/home/delta/work/mysite2/reddit/lib")

# *****************************************************************************
# Set up logger
from reddit.config import initializeCLogger
initializeCLogger()



