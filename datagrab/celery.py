from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datagrab.settings')

app = Celery('datagrab', broker='redis://localhost:6379/0')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Config options
# Restart worker after changing these
app.conf.worker_log_color=False
app.conf.worker_hijack_root_logger=False
app.conf.worker_log_format='%(asctime)-8s %(levelname).1s %(filename)-18s (line %(lineno)4s): %(message)s'

# ref: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
app.conf.timezone='Canada/Eastern'

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
