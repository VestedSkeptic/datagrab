from django.http import HttpResponse
from .comments import comments_updateForAllUsers

# *****************************************************************************
def updateComments(request):
    s = comments_updateForAllUsers()
    return HttpResponse(s)














