from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^praw/$',         views.main,                                 name='main'),
    url(r'^praw/ucfau/$',   views.updateCommentsForAllUsers,            name='updateCommentsForAllUsers'),
    url(r'^praw/usfas/$',   views.updateSubmissionsForAllSubreddits,    name='updateSubmissionsForAllSubreddits'),
    url(r'^praw/ucfas/$',   views.updateCommentsForAllSubmissions,      name='updateCommentsForAllSubmissions'),
    url(r'^cis/$',          views.checkInternetStatus,                  name='checkInternetStatus'),
]



