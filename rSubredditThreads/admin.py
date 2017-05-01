from django.contrib import admin

from .models import subreddit
from .models import subredditThreadProcessedStatus
from .models import subredditThreadIndex
from .models import subredditThreadRaw

admin.site.register(subreddit)
admin.site.register(subredditThreadProcessedStatus)
admin.site.register(subredditThreadIndex)
admin.site.register(subredditThreadRaw)



