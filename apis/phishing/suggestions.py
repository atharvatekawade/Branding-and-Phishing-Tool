import tldextract
import requests
import re
from bs4 import BeautifulSoup
from .similarity import Similarity

class Suggestions:
    def __init__(self,url,num=100):
        self.suggested_urls=[]
        self.found=0
        self.err=0
        self.num=str(num)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        }


        if(url[:4]!='http'):
            url='https://'+url

        r=tldextract.extract(url)
        
        self.original_domain=r.domain
        self.original_subdomain=r.subdomain
        try:
            # res=requests.get(url,headers=headers,timeout=3)
            # self.query_string=self.original_subdomain + "." + self.original_domain
            self.query_string = self.original_domain
            # soup=BeautifulSoup(res.content,"lxml")
            # for title in soup.find_all('title'):
            #     query_string=query_string+'%20'+title.get_text()
            print("Query string:",self.query_string)
        except:
            self.err=1

    def detect(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        }
        try:
            page = requests.get(f"https://www.bing.com/search?q={self.query_string}",headers=headers,timeout=3)
            print(f"https://www.bing.com/search?q={self.query_string}")
        except:
            self.err=1
            print("Error extracting")

        soup = BeautifulSoup(page.content,"lxml")
        links = soup.findAll("cite")
        i=0
        useful_links=[]
        print("Links:", links)
        for link in links:
            bing_url=str(link)[6:-7]
            r=tldextract.extract(bing_url)
            '''if(self.num=="100"):
                print(google_url)
                print(r.subdomain,r.domain)'''
            if(i>=int(self.num)):
                break
            if(r.domain==self.original_domain and r.subdomain==self.original_subdomain):
                print("Found url SE")
                self.found=1
                return
            
            sim=Similarity(self.original_domain,r.domain)
            sim.final_score()
            useful_links.append((bing_url,sim.score))
            i=i+1
        
        useful_links=sorted(useful_links, key=lambda x: x[1], reverse=True)
        some_links=[]
        for i in useful_links:
            if(i[0] not in some_links):
                r=tldextract.extract(i[0])
                if(r.domain!=self.original_domain or r.subdomain!=self.original_subdomain):
                    some_links.append(i[0])
                if(len(some_links)>=10):
                    break
        self.suggested_urls=some_links