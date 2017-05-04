from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^praw/uc/$',   views.updateCommentsForAllUsers,       name='updateCommentsForAllUsers'),
    url(r'^praw/ut/$',   views.updateThreadsForAllSubreddits,   name='updateThreadsForAllSubreddits'),
]