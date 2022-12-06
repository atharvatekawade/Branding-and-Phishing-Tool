import tldextract


class Domain_generator():
    Protocol=['https']

    class Helper():

        keyboards={'1': '2lqa', '2': '3wq1za', '3': '4ew2z', '4': '5re3', '5': '6tr4', '6': '7yt5z', '7': '8uy6z', '8': '9iu7', '9': '0oi8', '0': 'po9', 'q': '12wazs', 'w': '3esaq2x', 'e': '4rdsw3z', 'r': '5tfde4', 't': '6ygfr5z', 'y': '7uhgt6asx', 'u': '8ijhy7z', 'i': '9okju8', 'o': '0plki9', 'p': 'lo0m', 'a': 'qwszy21', 's': 'edxzawyq', 'd': 'rfcxse', 'f': 'tgvcdr', 'g': 'yhbvftz', 'h': 'ujnbgyz', 'j': 'ikmnhu', 'k': 'olmji', 'l': '1kopm', 'z': 'asx7uhgt63eq2', 'x': 'zsdcyw', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhjm', 'm': 'njklp'}

        def __init__(self,word):
            self.word=word

        def bitsquatting(self):
            result=[]
            masks=[]
            for i in range(7):
                masks.append(1<<i)
            
            for i in range(0, len(self.word)):
                w=self.word[i]
                for j in range(0, len(masks)):
                    b = chr(ord(w) ^ masks[j])
                    o=ord(b)
                    if (o >= 48 and o <= 57) or (o >= 97 and o <= 122) or o == 45:
                        result.append(self.word[:i] + b + self.word[i+1:])
            return result

        
        def vowel_swap(self):
            vowels=['a','e','i','o','u']
            result=[]
            for i in range(0, len(self.word)):
                if self.word[i] in vowels:
                    for vowel in vowels:
                        result.append(self.word[:i] + vowel + self.word[i+1:])
            return list(set(result))

        
        
        def add_on(self):
            result = []
            for i in range(97, 123):
                result.append(self.word + chr(i))
            return result

        def hyphenation(self):
            result = []
            for i in range(1, len(self.word)):
                result.append(self.word[:i] + '-' + self.word[i:])
            return result

        def insertion(self):
            result = []
            for i in range(1, len(self.word)-1):
                if self.word[i] in self.keyboards:
                        for c in self.keyboards[self.word[i]]:
                            result.append(self.word[:i] + c + self.word[i] + self.word[i+1:])
                            result.append(self.word[:i] + self.word[i] + c + self.word[i+1:])
            return list(set(result))

        def repetition(self):
            result = []
            for i in range(0, len(self.word)):
                if self.word[i].isalnum():
                    result.append(self.word[:i] + self.word[i] + self.word[i] + self.word[i+1:])
            return list(set(result))

        def replacement(self):
            result = []
            for i in range(0, len(self.word)):
                if self.word[i] in self.keyboards:
                    for c in self.keyboards[self.word[i]]:
                            result.append(self.word[:i] + c + self.word[i+1:])
            return list(set(result))
        
        def transposition(self):
            result = []
            for i in range(0, len(self.word)-1):
                if self.word[i+1] != self.word[i]:
                    result.append(self.word[:i] + self.word[i+1] + self.word[i] + self.word[i+2:])
            return result

        def generate_words(self):
            possibilities=self.bitsquatting()+self.vowel_swap()+self.add_on()+self.hyphenation()+self.insertion()+self.repetition()+self.replacement()+self.transposition()
            res = []
            [res.append(x) for x in possibilities if x not in res]
            return res

    def __init__(self,url):
        r=tldextract.extract(url)
        self.subdomain=r.subdomain
        self.Protocol='http://'
        self.domain=r.domain
        self.tlds=['org', 'com', 'net', 'gov', 'edu', 'co', 'mil', 'nom', 'ac', 'info', 'biz']
        if(r.suffix not in self.tlds):
            self.tlds.append(r.suffix)
    
    def generate_urls(self):
        #https://www.google.com/
        results=[]
        if(self.subdomain==''):
            self.subdomain='www'
        
    
        '''if(self.subdomain=='www'):
            h1=self.Helper(self.domain)

            for protocol in self.Protocol:
                for domain in h1.generate_words():
                    for tld in self.tlds:
                        results.append(protocol+'://www.'+domain+'.'+tld+'/')
        
        else:
            h1=self.Helper(self.domain)
            h2=self.Helper(self.subdomain)

            print('I am here')

            for protocol in self.Protocol:
                for domain in h1.generate_words():
                    if(domain!=self.domain):
                        for subdomain in h2.generate_words():
                            for tld in self.tlds:
                                results.append(protocol+'://'+subdomain+'.'+domain+'.'+tld+'/')
            
        print(len(results))
        #results=[]'''

        h1=self.Helper(self.domain)

        for domain in h1.generate_words():
            if(domain!=self.domain):
                for tld in self.tlds:
                    results.append(self.Protocol+self.subdomain+'.'+domain+'.'+tld)
        #print(len(results))

        return sorted(results)


'''url="www.google.com"
g=Domain_generator(url)
possible_urls=sorted(g.generate_urls())

with open('gen.txt', 'w') as f:
    for item in possible_urls:
        f.write("%s\n" % item)'''

#domainName='digitalocean.com'
#w = whois.whois(domainName)
#print(str(w.creation_date))












     





