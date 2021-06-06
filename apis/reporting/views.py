from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Report,Verify
from phishing.models import Fraud
import datetime
from datetime import date
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage,send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .utils import account_activation_token
import requests

# Create your views here.


def activate(request, uidb64, token):
    url=request.GET.get('p', '').lower()
    x = datetime.datetime.now()
    data={'report':0,'err':0}
    today=str(x.day)+'-'+str(x.month)+'-'+str(x.year)
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.delete()
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
    else:
        data['err']=1

    return JsonResponse(data,safe=False)

def report(request):
    factor=0.3
    data={'sent':0,'exceed':0,'err':0}
    url=request.GET.get('p', '').lower()
    confirmation=request.GET.get('q', '').lower()
    print(f"Reporting {url} from person {confirmation}")
    if(url[:4]!='http'):
        url="https://"+url

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }
    original_text=-1
    for j in range(2):
        res=-1
        try:
            if(j==0):
                res=requests.get(url,headers=headers,timeout=3)
            else:
                res=requests.get(url,headers=headers,timeout=8)
            if(res):
                original_text=res.text
                break
            else:
                data['err']=1
                break

        except requests.exceptions.Timeout:
            if(j==1):
                data['err']=1
                break
            
        except:
            data['err']=1
            break
    
    #print("Original text is",original_text)
    if(data['err']!=1):
        id='0'
        if request.COOKIES.get('id'):
            id=request.COOKIES['id']
        
        early=list(Verify.objects.filter(url=url,identity=id))
        if(len(early)>0):
            print("Already reported")
            data['exceed']=1
        
            return JsonResponse(data,safe=False)

        try:
            user=User.objects.get(username=id)
            if user:
                user.delete()
        except Exception:
            pass

        user = User.objects.create_user(username=id)
        user.set_password(id)
        user.save()

        domain = get_current_site(request).domain
        link = reverse('activate', kwargs={'uidb64':urlsafe_base64_encode(force_bytes(user.pk)),'token': account_activation_token.make_token(user)})
        activate_url = 'http://'+domain+link+'?p='+url
        subject='Verification link'
        body=f'Hi, Please find the link below to activate your account \n {activate_url}'

        email=EmailMessage(
            subject,
            body,
            'noreply@semycolon.com',
            [confirmation],
        )

        email.send(fail_silently=True)
        print("Email sent.....")
        data['sent']=1
    return JsonResponse(data,safe=False)
    
        
