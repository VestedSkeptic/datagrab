from django.conf.urls import url
from .views import vbase
from .views import vsubreddit
from .views import vthread
from .views import vuser

urlpatterns = [
    url(r'^vbase/main/$',                               vbase.main,                     name='vbase.main'),
    url(r'^vbase/main/xData/(?P<xData>\w+)/$',          vbase.main,                     name='vbase.main'),

    url(r'^vuser/list/$',                               vuser.list,                     name='vuser.list'),
    url(r'^vuser/add/(?P<name>\w+)/$',                  vuser.add,                      name='vuser.add'),
    url(r'^vuser/delAll/$',                             vuser.delAll,                   name='vuser.delAll'),
    url(r'^vuser/update/$',                             vuser.update,                   name='vuser.update'),

    url(r'^vsubreddit/list/$',                          vsubreddit.list,                name='vsubreddit.list'),
    url(r'^vsubreddit/add/(?P<name>\w+)/$',             vsubreddit.add,                 name='vsubreddit.add'),
    url(r'^vsubreddit/delAll/$',                        vsubreddit.delAll,              name='vsubreddit.delAll'),
    url(r'^vsubreddit/update/$',                        vsubreddit.update,              name='vsubreddit.update'),

    url(r'^vthread/delAll/$',                           vthread.delAll,                 name='vthread.delAll'),
    url(r'^vthread/update/$',                           vthread.update,                 name='vthread.update'),
    url(r'^vthread/list/(?P<subreddit>\w+)/$',          vthread.list,                   name='vthread.list'),
]



