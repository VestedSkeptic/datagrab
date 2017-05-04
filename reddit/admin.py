from django.contrib import admin

from .models import user
from .models import userCommentsProcessedStatus
from .models import userCommentsIndex
from .models import userCommentsRaw
from .models import subreddit
from .models import subredditThreadProcessedStatus
from .models import subredditThreadIndex
from .models import subredditThreadRaw

admin.site.register(user)
admin.site.register(userCommentsProcessedStatus)
admin.site.register(userCommentsIndex)
admin.site.register(userCommentsRaw)
admin.site.register(subreddit)
admin.site.register(subredditThreadProcessedStatus)
admin.site.register(subredditThreadIndex)
admin.site.register(subredditThreadRaw)
