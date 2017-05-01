from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',      views.index,                    name='index'),
    url(r'^uc/$',   views.updateComments,           name='updateComments'),
    url(r'^ut/$',   views.updateSubredditThreads,   name='updateSubredditThreads'),
]