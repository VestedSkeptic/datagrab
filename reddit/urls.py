from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^praw/$',         views.main,                                 name='main'),
    url(r'^praw/ucfau/$',   views.updateCommentsForAllUsers,            name='updateCommentsForAllUsers'),
    url(r'^praw/usfas/$',   views.updateSubmissionsForAllSubreddits,    name='updateSubmissionsForAllSubreddits'),
    url(r'^praw/ucfas/$',   views.updateCommentsForAllSubmissions,      name='updateCommentsForAllSubmissions'),
    url(r'^praw/dau/$',     views.deleteAllUsers,                       name='deleteAllUsers'),
    url(r'^praw/das/$',     views.deleteAllSubreddits,                  name='deleteAllSubreddits'),
    url(r'^praw/da/$',      views.deleteAll,                            name='deleteAll'),

    url(r'^praw/auser/(?P<uname>\w+)/$', views.addUser,                 name='addUser'),
    url(r'^praw/asub/(?P<sname>\w+)/$',  views.addSub,                  name='addSub'),
    url(r'^praw/aboth/(?P<uname>\w+)/(?P<sname>\w+)/$', views.addBoth,  name='addBoth'),

    url(r'^praw/pch/(?P<hLevel>\w+)/$', views.parseCommentHeirarchy,    name='parseCommentHeirarchy'),

    url(r'^praw/ssfe/$',    views.deleteAllSSFE,                        name='deleteAllSSFE'),

    url(r'^praw/usrsfe/$',  views.updateSSFE,                           name='updateSSFE'),
]



