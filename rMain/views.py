from django.http import HttpResponse

# *****************************************************************************
def index(request):
    s  = ''
    s += '<br><a href="http://localhost:8000/admin/">admin</a>'
    s += '<br>'
    s += '<br><a href="http://localhost:8000/reddit/uc/">update users comments</a>'
    s += '<br>'
    s += '<br><a href="http://localhost:8000/reddit/ut/">update subreddit threads</a>'
    s += '<br>'
    s += '<br><a href="http://localhost:8000/reddit/utc/">update subreddit comments</a>'
    s += '<br>'

    s += '<br><b>PRAW</b> <a href="http://localhost:8000/reddit/praw/uc/">update user comments</a>'
    s += '<br>'
    s += '<br><b>PRAW</b> <a href="http://localhost:8000/reddit/praw/ut/">update subreddit threads</a>'
    s += '<br>'
    return HttpResponse(s)















