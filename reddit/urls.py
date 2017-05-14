from django.conf.urls import url
from .views import views
from .views import vbase
from .views import vuser
from .views import vsubreddit
from .views import vthread

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








    url(r'^vbase/main/$',                       vbase.main,             name='vbase.main'),
    url(r'^vbase/main/xData/(?P<xData>\w+)/$',  vbase.main,             name='vbase.main'),

    url(r'^vuser/list/$',                       vuser.list,             name='vuser.list'),
    url(r'^vuser/add/(?P<name>\w+)/$',          vuser.add,              name='vuser.add'),
    url(r'^vuser/delAll/$',                     vuser.delAll,           name='vuser.delAll'),
    url(r'^vuser/update/$',                     vuser.update,           name='vuser.update'),

    url(r'^vsubreddit/list/$',                  vsubreddit.list,        name='vsubreddit.list'),
    url(r'^vsubreddit/add/(?P<name>\w+)/$',     vsubreddit.add,         name='vsubreddit.add'),
    url(r'^vsubreddit/delAll/$',                vsubreddit.delAll,      name='vsubreddit.delAll'),
    url(r'^vsubreddit/update/$',                vsubreddit.update,      name='vsubreddit.update'),

    url(r'^vthread/list/$',                 vthread.list,       name='vthread.list'),
    url(r'^vthread/delAll/$',               vthread.delAll,     name='vthread.delAll'),
]



