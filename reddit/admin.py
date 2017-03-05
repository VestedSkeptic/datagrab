from django.contrib import admin
from .models import user
from .models import userCommentsProcessedStatus
from .models import userCommentsIndex
from .models import userCommentsRaw

admin.site.register(user)
admin.site.register(userCommentsProcessedStatus)
admin.site.register(userCommentsIndex)
admin.site.register(userCommentsRaw)

