from django.http import HttpResponse
from .comments import comments_updateForAllUsers
# import json

# *****************************************************************************
def index(request):
    s  = '<b> LINKS </b>'
    s += '<br><a href="http://localhost:8000/reddit/uc/">get comments for all users</a>'
    s += '<br>'
    s += '<br><a href="http://localhost:8000/admin/">admin</a>'
    return HttpResponse(s)

# *****************************************************************************
def updateComments(request):
    s = comments_updateForAllUsers()
    return HttpResponse(s)















