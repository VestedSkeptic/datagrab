from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^uc/$',   views.updateComments,           name='updateComments'),
]