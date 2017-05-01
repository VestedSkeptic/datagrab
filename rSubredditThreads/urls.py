from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^ut/$',   views.updateSubredditThreads,   name='updateSubredditThreads'),
]