from django.http import HttpResponse
from .comments import comments_updateForAllUsers
# from django.shortcuts import render

# *****************************************************************************
def updateCommentsForAllUsers(request):
    s = comments_updateForAllUsers()
    return HttpResponse(s)