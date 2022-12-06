from django.shortcuts import render
from django.http import JsonResponse
from concurrent.futures import ThreadPoolExecutor
import datetime
from datetime import date
# from html_similarity import style_similarity, structural_similarity, similarity
import requests
from .generator import Domain_generator
from .models import Url
from main.models import Person
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def similarity(d1, d2):
    corpus = [d1, d2]
    # Initialize an instance of tf-idf Vectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Generate the tf-idf vectors for the corpus
    tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

    # compute and print the cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    return cosine_sim[0][1]

def fetch(url,d,original_text):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }
   
    for j in range(2):
            res=-1
            try:
                if(j==0):
                    res=requests.get(url,headers=headers,timeout=3)
                else:
                    #print('I came here')
                    res=requests.get(url,headers=headers,timeout=8)
                if(res):
                    #print(f'Success site {possible_urls[i]}')
                    d[url]=str(round(similarity(str(res.text),original_text)*100,2))
                    #print(f'{i}. {possible_urls[i]} --> {responses[i]} %')
                    break
                
                else:
                    break

            except requests.exceptions.Timeout:
                if(j==1):
                    break
            
            except Exception:
                break

# Create your views here.

def scan(request):
    print('This is a view')
    x = datetime.datetime.now()
    data={}
    data['urls']=[]
    data['err']=0
    data['exceed']=0

    today=str(x.day)+'-'+str(x.month)+'-'+str(x.year)
    #print("Today is",today)
    if request.COOKIES.get('id'):
        id=request.COOKIES['id']
        entity=list(Person.objects.filter(identity=id,updated=today,category='branding'))
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
            Person.objects.filter(identity=id,category='branding').delete()
            Person.objects.create(identity=id,updated=today,category='branding',count=1)

    workers=100

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }

    url=request.GET.get('q', '').lower()
    p=request.GET.get('p', '').lower()

    try:
        p=float(p)
    except ValueError:
        p=20

    if(url[0:4]!='http'):
        url='https://'+url
    
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
    
    
    print("Hey I entered here",url,p)
    if(data['err']==1):
        return JsonResponse(data,safe=False)

    urls=list(Url.objects.filter(main=url))
    #print(urls)
    flag=0

    if(len(urls)>0):
        last_update=urls[0].updated.split('-')
        f_date = date(int(last_update[2]),int(last_update[1]),int(last_update[0]))
        delta = x.date()-f_date
        if(delta.days<=3):
            flag=1
            print("It is there in db")
            for u in urls:
                if(float(u.score)>=p):
                    data['urls'].append({'url':u.similar,'score':float(u.score)})
            #return JsonResponse(data,safe=False)

    
    if(flag==0):
        Url.objects.filter(main=url).delete()
        if(original_text!=1):

            g=Domain_generator(url)
            possible_urls=g.generate_urls()
            d={}

            print("Search space",len(possible_urls))

            for i in possible_urls:
                #responses.append(-1)
                d[i]=-1
                

            #print("Hey there")

            '''threads = list()
            for index in range(workers):
                x = threading.Thread(target=thread_function, args=(index,possible_urls,responses,original_text,workers,headers,))
                threads.append(x)
                x.start()

            for thread in threads:
                thread.join()'''

            with ThreadPoolExecutor(max_workers=workers) as executor:
                executor.map(fetch, possible_urls,[d]*len(possible_urls),[original_text]*len(possible_urls))
                executor.shutdown(wait=True)
            
            j=1
            '''for i in range(len(possible_urls)):
                if(responses[i]!=-1):
                    Url.objects.create(main=url,similar=possible_urls[i],score=responses[i],updated=today)
                    #if(find(data['urls'],possible_urls[i])==0):
                    if(responses[i]>=p):
                        data['urls'].append({'url':possible_urls[i],'similarity':round(responses[i],2)})'''

            for i in possible_urls:
                if(d[i]!=-1):
                    Url.objects.create(main=url,similar=i,score=d[i],updated=today)
                    if(float(d[i])>=p):
                        data['urls'].append({'url':i,'score':float(d[i])})

            if(len(data['urls'])==0):
                Url.objects.create(main=url,similar=url,score='100.00',updated=today)
                data['urls'].append({'url':url,'score':100})


        else:
            data['err']=1
            print("Wrong supplied url")

    data['urls']=sorted(data['urls'], key=lambda k: k['score'],reverse=True) 
    print('Finished',len(data['urls']))

    return JsonResponse(data,safe=False)


def similar(request):
    main=request.GET.get('q1', '').lower()
    copy=request.GET.get('q2', '').lower()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }
    print("Hey I entered here",main,copy)
    data={}
    data['score']=0
    data['err']=0

    if(main[:4]!='http'):
        main='https://'+main

    if(copy[:4]!='http'):
        copy='https://'+copy

    original_text=''
    new_text=''

    for j in range(2):
        res=-1
        try:
            if(j==0):
                res=requests.get(main,headers=headers,timeout=3)
            else:
                res=requests.get(main,headers=headers,timeout=8)
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

    if(data['err']==0):

        for j in range(2):
            res=-1
            try:
                if(j==0):
                    res=requests.get(copy,headers=headers,timeout=3)
                else:
                    res=requests.get(copy,headers=headers,timeout=8)
                if(res):
                    new_text=res.text
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
        
    #data['score']=round(sim(new_text,original_text)*100,2)
    data['score']=round(similarity(new_text,original_text)*100,2)
    print(data['score'])
    if(data['err']==1):
        print("Something went wrong!!")
    return JsonResponse(data,safe=False)
