from django.shortcuts import render
from django.http import JsonResponse
import datetime
from datetime import date
import sklearn
import joblib
from .models import Fraud
from main.models import Person
from .suggestions import Suggestions
from .features import Features

# Create your views here.


def phis(request):
    x = datetime.datetime.now()
    today=str(x.day)+'-'+str(x.month)+'-'+str(x.year)

    data={}
    data['suggested_urls']=[]
    data['err']=0
    data['exceed']=0


    if request.COOKIES.get('id'):
        id=request.COOKIES['id']
        entity=list(Person.objects.filter(identity=id,updated=today,category='phising'))
        if(len(entity)>0):
            count=entity[0].count
            if(count>=5):
                data['exceed']=1
                print("Limit Exceeded",entity[0].identity,entity[0].updated,entity[0].count)
                return JsonResponse(data,safe=False)
            else:
                entity[0].count=count+1
                entity[0].save()
        else:
            Person.objects.filter(identity=id,category='phising').delete()
            Person.objects.create(identity=id,updated=today,category='phising',count=1)

    url=request.GET.get('p', '').lower()
    if(url[:4]!='http'):
        url='https://'+url
    
    
    print("Entered here successfully",url)
    entity=list(Fraud.objects.filter(url=url))

    finder=Suggestions(url)
    if(finder.err==1):
        print("Some error occured")
        data['err']=1
        return JsonResponse(data,safe=False)
    finder.detect()
    if(finder.err==1):
        print("Some error occured")
        data['err']=1
        return JsonResponse(data,safe=False)

    if(len(entity)>0):
        print("Phising site DB")
        if(len(finder.suggested_urls)==0):
            data['suggested_urls'].append('https://www.google.com/')
        else:
            data['suggested_urls']=finder.suggested_urls
        return JsonResponse(data,safe=False)

    if(finder.found==1):
        print("Not a phising site SE method")
        return JsonResponse(data,safe=False)
    
    extractor=Features(url)
    extractor.extract()
    if(extractor.err==1):
        print("Some error occured")
        data['err']=1
        return JsonResponse(data,safe=False)

    classifier = joblib.load('ML/rf_final.pkl')
    prediction=classifier.predict(extractor.features)[0]

    print("Prediction is",prediction)

    if(prediction!=-1):
        print("Phising website")
        #data['suggested_urls']=extractor.suggested_urls
        if(len(finder.suggested_urls)==0):
            data['suggested_urls'].append('https://www.google.com/')
        else:
            data['suggested_urls']=finder.suggested_urls
    else:
        print("Not phising website")  
    return JsonResponse(data,safe=False)