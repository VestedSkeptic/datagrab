from django.http import HttpResponse
from .comments import comments_updateForAllUsers
# import json

# *****************************************************************************
def index(request):
    s  = '<b> INDEX </b>'
    s += '<br><a href="http://localhost:8000/reddit/uc/">comments_updateForAllUsers</a>'
    s += '<br><a href="http://localhost:8000/reddit/a/">credentials_get</a>'
    s += '<br>'
    s += '<br><a href="http://localhost:8000/admin/">admin</a>'
    return HttpResponse(s)

# *****************************************************************************
def updateComments(request):
    s = comments_updateForAllUsers()
    return HttpResponse(s)

# *****************************************************************************
def access(request):
    return HttpResponse("ACCESS VIEW")


# OldDevLearningLinux:
# OldDevLearningLinux: AA: [After: NOT processed] [Before: NOT processed]
# commentQuery: https://oauth.reddit.com/user/OldDevLearningLinux/comments/.json
# DATA: AFTER: t1_dejdd7m, BEFORE: None, MODHASH: , CHILDREN: 25
# 1: t1_dejeekt Reply 26a
# 2: t1_dejdfgu Reply 25a
# 3: t1_dejdfdu Reply 24a
# 4: t1_dejdfb2 Reply 23a
# 5: t1_dejdf88 Reply 22a
# 6: t1_dejdf5s Reply 21a
# 7: t1_dejdf15 Reply 20a
# 8: t1_dejdewe Reply 19a
# 9: t1_dejderj Reply 18a
# 10: t1_dejdeoy Reply 17a
# 11: t1_dejdem6 Reply 16a
# 12: t1_dejdejh Reply 15a
# 13: t1_dejdefc Reply 14a
# 14: t1_dejdece Reply 13a
# 15: t1_dejde9u Reply 12a
# 16: t1_dejde7w Reply 11a
# 17: t1_dejde3q Reply 10a
# 18: t1_dejddwl Reply 09a
# 19: t1_dejddty Reply 08a
# 20: t1_dejddqf Reply 07a
# 21: t1_dejddo6 Reply 06a
# 22: t1_dejddl6 Reply 05a
# 23: t1_dejddid Reply 04a
# 24: t1_dejddeu Reply 03a
# 25: t1_dejdd7m Reply 02a
# youngestChild = t1_dejeekt
# OldDevLearningLinux: BB: [After: t1_dejdd7m] [Before: t1_dejeekt]

# OldDevLearningLinux:
# OldDevLearningLinux: AA: [After: t1_dejdd7m] [Before: t1_dejeekt]
# commentQuery: https://oauth.reddit.com/user/OldDevLearningLinux/comments/.json?after=t1_dejdd7m
# DATA: AFTER: None, BEFORE: None, MODHASH: , CHILDREN: 5
# 1: t1_dejdcxn Reply 01abb
# 2: t1_dejdcjp Reply 01aba
# 3: t1_dejdc9t Reply 01ab
# 4: t1_dejdate Reply 01aa
# 5: t1_dejda4f Reply 01a
# youngestChild = t1_dejdcxn
# OldDevLearningLinux: BB: [After: processed] [Before: t1_dejeekt]

# OldDevLearningLinux:
# OldDevLearningLinux: AA: [After: processed] [Before: t1_dejeekt]
# commentQuery: https://oauth.reddit.com/user/OldDevLearningLinux/comments/.json?before=t1_dejeekt
# DATA: AFTER: None, BEFORE: None, MODHASH: , CHILDREN: 0
# youngestChild =
# OldDevLearningLinux: BB: [After: processed] [Before: t1_dejeekt]

# ADDED NEW REPLY ON Reddit


















