from django.contrib import admin
from .models import user, userCommentsProcessedStatus

admin.site.register(user)
admin.site.register(userCommentsProcessedStatus)

