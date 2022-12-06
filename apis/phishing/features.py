import tldextract
import ssl
import whois
import socket
import favicon
import requests
from bs4 import BeautifulSoup
#from selenium import webdriver
import datetime
import dns.resolver
import joblib
import re
import ipaddress
from urllib.parse import urlencode
from .suggestions import Suggestions
from urllib.parse import urlencode
from urllib.request import urlopen


class Features:
    
    def __init__(self,url):
        self.url=url
        self.features=[[]]
        self.text=''
        self.who=''
        self.domain=tldextract.extract(url).domain
        self.subdomain=tldextract.extract(url).subdomain
        self.suffix=tldextract.extract(url).suffix
        self.redirects=0
        self.dns=0
        self.err=0
        self.detect=-1

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        }

        try:
            res=requests.get(url,headers=headers,timeout=3)
            self.text=res.text
            self.redirects=len(res.history)
        except:
            self.err=1
            print("Error while site") 
            return
        
        try:
            host_name=self.domain+'.'+self.suffix
            self.who=whois.whois(host_name)
        except:
            print("Error while getring who")
            
        try:
            host_name=self.domain+'.'+self.suffix
            my_resolver = dns.resolver.Resolver()
            answers = my_resolver.resolve(host_name, "A")
            self.dns=len(answers)
        
        except:
            print("Error while getting dns")
    
    def ip(self):
        ret_val=-1
        try:
            ipaddress.ip_address(self.url)
            ret_val = 1
        except:
            pass
        return ret_val
    
    def url_length(self):
        l=0
        #https://www.youtube.com/
        if(self.url[0:5]=='https'):
            l=len(self.subdomain)+len(self.domain)+len(self.suffix)+10
        else:
            l=len(self.subdomain)+len(self.domain)+len(self.suffix)+9
        if(l<54):
            return -1
        elif(l>=54 and l<=75):
            return 0
        else:
            return 1
    
    def tiny_url(self):
        shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"
        match=re.search(shortening_services,self.url)
        if match:
            return 1
        else:
            return -1
   
    def at_present(self):
        url=self.url
        for i in url:
            if(i=='@'):
                return 1
        
        return -1
    
    def double_slash(self):
        url=self.url
        positions=0
        for i in range(len(url)-1):
            if(url[i:i+2]=='//'):
                positions=positions+1
        
        if(positions>1):
            return 1
        return -1
    
    def prefix_suffix(self):
        if(self.domain.count('-')>0):
            return 1
        else:
            return -1
    
    def subdomain_dot(self):
        cnt=self.subdomain.count('.')
        if(cnt==0):
            return -1
        elif(cnt==1):
            return 0
        else:
            return 1
    
    def verify_ssl(self):
        https=0
        url=self.url
        if(url[:5]=="https"):
            https=1
        
        host_name=self.domain+'.'+self.suffix

        try:
            context = ssl.create_default_context()
            sct = context.wrap_socket(socket.socket(), server_hostname = host_name)
            sct.connect((host_name, 443))
            certificate = sct.getpeercert()
            issuer = dict(x[0] for x in certificate['issuer'])
            certificate_Auth = str(issuer['commonName'])
            certificate_Auth = certificate_Auth.split()
            if(certificate_Auth[0] == "Network" or certificate_Auth == "Deutsche"):
                certificate_Auth = certificate_Auth[0] + " " + certificate_Auth[1]
            else:
                certificate_Auth = certificate_Auth[0] 
            trusted_Auth = ['Comodo','Symantec','GoDaddy','GlobalSign','DigiCert','StartCom','Entrust','Verizon','Trustwave','Unizeto','Buypass','QuoVadis','Deutsche Telekom','Network Solutions','SwissSign','IdenTrust','Secom','TWCA','GeoTrust','Thawte','Doster','VeriSign','GTS']

            print("SSL here")
            present=0
            if(certificate_Auth in trusted_Auth):
                present=1

            startingDate = str(certificate['notBefore'])
            endingDate = str(certificate['notAfter'])
            startingYear = int(startingDate.split()[3])
            endingYear = int(endingDate.split()[3])
            age = endingYear-startingYear

            print(age,certificate_Auth)

            if(https==1 and present==1 and age>=1):
                print("Valid")
                return -1
            elif(https==1 and present==1):
                print("Suspicious")
                return 0
            elif(https==1 and age>=1):
                return 0
            else:
                print("Phis")
                return 1
        except:
            print("Some err")
            return 0

    def domain_registration(self):
        if(self.who!=''):
            try:
                w = self.who
                updated = w.updated_date
                exp = w.expiration_date
                print(updated)
                print(exp)
                try:
                    exp=exp[0]
                except:
                    pass
                
                try:
                    updated=updated[0]
                except:
                    pass
                length = (exp-updated).days
                if(length<=365):
                    return 1
                else:
                    return -1
            except:
                print("Some error ocurred while processing")
                return 0
        else:
            return 0


    def favicon(self):
        #print("Getting favicons")
        url=self.url
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        }
        try:
            #print("Try block of favicons")
            icons=favicon.get(url,headers=headers,timeout=3)
            #icons=favicon.get(url)
            for icon in icons:
                icon_domain=tldextract.extract(icon.url).domain
                if(icon_domain!=self.domain and icon_domain!=''):
                    #print("Finished favicons")
                    return 1
            #print("Finished favicons")
            return -1
        except:
            #print("Finished favicons")
            return 0
    
    def port(self):
        return 0
    
    def https_token(self):
        host =self.subdomain +'.' + self.domain + '.' + self.suffix 
        if(host.count('https')>0):
            return 1
        else:
            return -1

    def imgs_vid(self):
        txt=self.text
        soup = BeautifulSoup(txt, 'lxml')
        imgs = soup.findAll('img', src=True)
        diff=0

        for i in imgs:
            source=tldextract.extract(str(i['src'])).domain
            if(source!=self.domain and source!=''):
                diff=diff+1

        vids = soup.findAll('video', src=True)
        for i in vids:
            source=tldextract.extract(str(i['src'])).domain
            if(source!=self.domain and source!=''):
                diff=diff+1
        
        tot=len(imgs)+len(vids)

        if(tot==0):
            return -1
        
        avg=diff/tot

        if(avg<0.22):
            return -1
        
        if(avg<=0.61):
            return 0
        
        return 1


    def anchors(self):
        txt=self.text
        soup = BeautifulSoup(txt, 'lxml')
        anchors = soup.findAll('a', href=True)
        diff=0

        for i in anchors:
            ref=str(i['href'])
            source=tldextract.extract(ref).domain
            if(len(ref)>0 and ref[0]=='#'):
                diff=diff+1
            elif(source!='' and source!=self.domain):
                diff=diff+1  

        tot=len(anchors)
        if(tot==0):
            return -1

        avg=diff/tot

        if(avg<0.31):
            return -1

        if(avg<=0.67):
            return 0  

        return 1

    def links(self):
        txt=self.text
        soup = BeautifulSoup(txt, 'lxml')
        anchors = soup.findAll('a')
        metas= soup.findAll('meta')
        links = soup.find_all('link')
        scripts = soup.find_all('script')

        tot=len(anchors)+len(metas)+len(links)+len(scripts)
        others=tot-len(anchors)

        if(tot==0):
            return -1

        avg=others/tot

        if(avg<0.17):
            return -1

        if(avg<=0.81):
            return 0

        return 1

    def sfh(self):
        return 0

    def mail(self):
        soup=BeautifulSoup(self.text,'lxml')
        if(soup.find('mailto:')):
            return 1
        else:
            return -1 
    
    def abnormal(self):
        if(self.domain!=''):
            return -1
        
        return 1
    
    def num_redirects(self):
        if(self.redirects==0):
            return -1
        
        if(self.redirects<3):
            return 0
        
        return 1
    
    def mouseover(self):
        return 0
    
    def right_click(self):
        match=re.findall(r"event.button ?== ?2", self.text)
        if(match and len(match)>0):
            return 1
        else:
            return -1
    
    def popup(self):
        return 0
    
    def iframe(self):
        soup=BeautifulSoup(self.text,'lxml')
        for i in soup.findAll('iframe'):
            if('frameborder' in i.attrs):
                return 1
        
        return -1

    def domain_age(self):
        w=self.who
        if(w!=''):
            try:
                start_date = w.creation_date
                try:
                    start_date=start_date[0]
                except:
                    pass

                current_date = datetime.datetime.now()
                age =(current_date-start_date[0]).days
                if(age>=180):
                    return -1
                else:
                    return 1
            except:
                return 0
        return 0

    def dns_count(self):
        if(self.dns>0):
            return -1
        return 1
    
    def traffic(self):
        return 0
    
    def page_rank(self):
        return 0
    
    def google_index(self):
        finder=Suggestions(self.url,1000)
        if(finder.err==0):
            finder.detect()
            if(finder.err==0):
                if(finder.found==1):
                    return -1
                else:
                    return 1
            return 0
        #return -1
    
    def links_pointing(self):
        return 0
    
    def stats(self):
        return 0
    
    def extract(self):
        if(self.err==1):
            return
        
        print("Extracting features")
        self.features=[[self.ip(),self.url_length(),self.tiny_url(),self.at_present(),self.double_slash(),self.prefix_suffix(),
                        self.subdomain_dot(),self.verify_ssl(),self.domain_registration(),self.favicon(),self.port(),self.https_token(),
                        self.imgs_vid(),self.anchors(),self.links(),self.sfh(),self.mail(),self.abnormal(),self.num_redirects(),
                        self.mouseover(),self.right_click(),self.popup(),self.iframe(),self.domain_age(),self.dns_count(),self.traffic(),
                        self.page_rank(),self.google_index(),self.links_pointing(),self.stats()
        ]]
        
        print("Features extracted",self.features[0])

        # Show phising example https://salty-bastion-77833.herokuapp.com/
        '''print("Showing phising features")
        for i in range(len(self.features[0])):
            self.features[0][i]=1'''


        
    

'''detector=Phising_Detection('https://github.com/')
detector.predict()
print(detector.detect)'''



        

