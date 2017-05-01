from django.http import HttpResponse
from .comments import comments_updateForAllUsers

# # *****************************************************************************
# def index(request):
#     s  = ''
#     s += '<br><a href="http://localhost:8000/admin/">admin</a>'
#     s += '<br>'
#     s += '<br><a href="http://localhost:8000/reddit/uc/">update users comments</a>'
#     s += '<br>'
#     s += '<br><a href="http://localhost:8000/reddit/ut/">update subreddit threads</a>'
#     s += '<br>'
#     return HttpResponse(s)

# *****************************************************************************
def updateComments(request):
    s = comments_updateForAllUsers()
    return HttpResponse(s)














