from django.conf.urls import url
from . import views
from . import vBase
from . import vUser
from . import vSubreddit

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








    url(r'^vBase/main/$',                       vBase.main,             name='vBase_main'),
    url(r'^vBase/main/xData/(?P<xData>\w+)/$',  vBase.main,             name='vBase_main'),

    url(r'^vUser/list/$',                       vUser.list,             name='vUser_list'),
    url(r'^vUser/add/(?P<name>\w+)/$',          vUser.add,              name='vUser_add'),
    url(r'^vUser/delAll/$',                     vUser.delAll,           name='vUser_delAll'),

    url(r'^vSubreddit/list/$',                  vSubreddit.list,        name='vSubreddit_list'),
    url(r'^vSubreddit/add/(?P<name>\w+)/$',     vSubreddit.add,         name='vSubreddit_add'),
    url(r'^vSubreddit/delAll/$',                vSubreddit.delAll,      name='vSubreddit_delAll'),
]



