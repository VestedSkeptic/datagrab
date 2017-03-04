from django.http import HttpResponse
from .comments import comments_updateForAllUsers
from .credentials import credentials_get

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
    s = credentials_get()
    return HttpResponse(s)













    # print ("TEST TEST TEST TEST TEST TEST TEST")
