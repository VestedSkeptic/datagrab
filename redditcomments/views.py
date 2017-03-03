# from django.shortcuts import render
from django.http import HttpResponse
from redditusers.models import reddituser
import requests

# def index(request):
#     r = requests.get('https://www.reddit.com/user/BeneficEvil/comments/.json')
#     d = r.json()
#     # return HttpResponse(d.keys())     # works
#     # return HttpResponse(d['kind'])    # works
#     # return HttpResponse(d['data']['modhash'])     #fails
#     # return HttpResponse(r, content_type="application/json") # works
#     # return HttpResponse(d['data']['children'][0]['kind'])     # works
#     # return HttpResponse(d['data']['children'][0]['data']['link_id']) #works
#     return HttpResponse(d['data']['children'][0]['data']['body']) #works
  
    
# Three queries to get user comments using after value from previous    
# https://www.reddit.com/user/stp2007/comments/.json    
# https://www.reddit.com/user/stp2007/comments/.json?after=t1_d8fi1ll
# https://www.reddit.com/user/stp2007/comments/.json?after=t1_d6b14um
     
    

def index(request):
    all_entries = reddituser.objects.all()
        
    s = "REDDIT COMMENTS VIEW: "
    for entry in all_entries:
        s += entry.username

    return HttpResponse(s) 
    
    
    
    
    