from django.contrib import admin

from .models import user
from .models import userCommentsProcessedStatus
from .models import userCommentsIndex
from .models import userCommentsRaw
from .models import subreddit
from .models import subredditSubmissionProcessedStatus
from .models import subredditSubmissionIndex
from .models import subredditSubmissionRaw

admin.site.register(user)
admin.site.register(userCommentsProcessedStatus)
admin.site.register(userCommentsIndex)
admin.site.register(userCommentsRaw)
admin.site.register(subreddit)
admin.site.register(subredditSubmissionProcessedStatus)
admin.site.register(subredditSubmissionIndex)
admin.site.register(subredditSubmissionRaw)
