from django.shortcuts import render
from django.http import JsonResponse
from .models import Report,Verify
from phishing.models import Fraud
import datetime
from datetime import date

# Create your views here.


def report(request):
    factor=0.3
    data={'report':0,'exceed':0}
    x = datetime.datetime.now()
    today=str(x.day)+'-'+str(x.month)+'-'+str(x.year)
    url=request.GET.get('p', '').lower()
    if(url[:4]!='http'):
        url="https://"+url

    id='0'
    if request.COOKIES.get('id'):
        id=request.COOKIES['id']
    
    early=list(Verify.objects.filter(url=url,identity=id))
    if(len(early)>0):
        print("Already reported")
        data['exceed']=1
        return JsonResponse(data,safe=False)
        
    entity=list(Report.objects.filter(url=url))
    Verify.objects.create(url=url,identity=id)

    if(len(entity)>0):
        last_update=entity[0].updated
        last_count=entity[0].count
        new_count=last_count+1
        Report.objects.filter(url=url).delete()
        if(last_update==today):
            Report.objects.create(url=url,updated=today,count=new_count)
            if(new_count>=25):
                Fraud.objects.create(url=url)
        else:
            last_update=last_update.split('-')
            f_date = date(int(last_update[2]),int(last_update[1]),int(last_update[0]))
            delta = x.date()-f_date
            if(delta.days<7):
                new_count=int(factor*last_count)+1
                Report.objects.create(url=url,updated=today,count=new_count)
                if(new_count>=25):
                    Fraud.objects.create(url=url)
            else:
                Report.objects.create(url=url,updated=today,count=1)
    else:
        Report.objects.create(url=url,updated=today,count=1)

    print("Reported successfully")
    data['report']=1
    return JsonResponse(data,safe=False)
