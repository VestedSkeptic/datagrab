from django.conf.urls import url
from .views import vbase
from .views import vsubreddit
from .views import vthread
from .views import vuser
from .views import vanalysis

urlpatterns = [
    url(r'^vbase/main/$',                               vbase.main,                         name='vbase.main'),
    url(r'^vbase/main/xData/(?P<xData>\w+)/$',          vbase.main,                         name='vbase.main'),
    url(r'^vbase/test/$',                               vbase.test,                         name='vbase.test'),

    url(r'^vuser/list/$',                               vuser.list,                         name='vuser.list'),
    url(r'^vuser/formNewPoiUser/$',                     vuser.formNewPoiUser,               name='vuser.formNewPoiUser'),

    url(r'^vsubreddit/list/$',                          vsubreddit.list,                    name='vsubreddit.list'),
    url(r'^vsubreddit/list/xData/(?P<xData>\w+)/$',     vsubreddit.list,                    name='vsubreddit.list'),
    url(r'^vsubreddit/formNewPoiSubreddit/$',           vsubreddit.formNewPoiSubreddit,     name='vsubreddit.formNewPoiSubreddit'),

    url(r'^vthread/list/(?P<subreddit>\w+)/$',          vthread.list,                       name='vthread.list'),

    url(r'^vanalysis/poiUsersOfSubreddit/(?P<subreddit>\w+)/(?P<minNumComments>\w+)/$',     vanalysis.poiUsersOfSubreddit,          name='vanalysis.poiUsersOfSubreddit'),
    url(r'^vanalysis/moderatorsOfSubreddit/(?P<subreddit>\w+)/$',                           vanalysis.moderatorsOfSubreddit,        name='vanalysis.moderatorsOfSubreddit'),


]






# url(r'^vuser/delAll/$',                             vuser.delAll,                   name='vuser.delAll'),
# url(r'^vsubreddit/delAll/$',                        vsubreddit.delAll,              name='vsubreddit.delAll'),
# url(r'^vthread/delAll/$',                           vthread.delAll,                 name='vthread.delAll'),

