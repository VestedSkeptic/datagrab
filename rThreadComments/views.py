from django.http import HttpResponse
from .threadComments import threadComments_updateForAll

# *****************************************************************************
def updateThreadComments(request):
    s = threadComments_updateForAll()
    return HttpResponse(s)













