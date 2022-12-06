from django.shortcuts import render
from django.http import HttpResponse
import random
import string
import time
from .models import Person
from monitoring.models import Url

# Create your views here.

def common(request):
    id=''.join(random.choices(string.ascii_uppercase +string.digits, k = 10))
    if request.COOKIES.get('id'):
        response = render(request, 'index.html',{'cookie':request.COOKIES['id']})
        print("There is cookie")
        print("Cookie is",request.COOKIES['id'])
    else:
        response = render(request, 'index.html',{'cookie':'No cookie'})
        response.set_cookie('id',id,time.time() + (10 * 365 * 24 * 60 * 60))
        print("There is no cookie")
        print("Cookie set to",id)
    return response

def flush(request,val):
    if(val=='g'):
        #"https://www.google.com",
        Url.objects.filter(main='https://www.google.com').delete()
        return HttpResponse("Deleted google")
    if(val!='p'):
        Url.objects.all().delete()
    Person.objects.all().delete()
    print("Objects deleted")
    return HttpResponse("Deleted")

