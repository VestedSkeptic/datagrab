from django.contrib import admin
from .models import user, userCommentProcessedStatus

admin.site.register(user)
admin.site.register(userCommentProcessedStatus)

