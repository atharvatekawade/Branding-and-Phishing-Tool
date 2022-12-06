import tldextract

class Domain_generator():
    Protocol=['https']

    class Helper():

        qwerty = {
            '1': '2ql', '2': '3wq1', '3': '4ew2', '4': '5re3', '5': '6tr4', '6': '7yt5', '7': '8uy6', '8': '9iu7', '9': '0oi8', '0': 'po9',
            'q': '12wa', 'w': '3esaq2', 'e': '4rdsw3', 'r': '5tfde4', 't': '6ygfr5', 'y': '7uhgt6', 'u': '8ijhy7', 'i': '9okju8', 'o': '0plki9', 'p': 'lo0',
            'a': 'qwsz', 's': 'edxzaw', 'd': 'rfcxse', 'f': 'tgvcdr', 'g': 'yhbvft', 'h': 'ujnbgy', 'j': 'ikmnhu', 'k': 'olmji', 'l': '1kop',
            'z': 'asx', 'x': 'zsdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhjm', 'm': 'njk'
            }
        qwertz = {
                '1': '2q', '2': '3wq1', '3': '4ew2', '4': '5re3', '5': '6tr4', '6': '7zt5', '7': '8uz6', '8': '9iu7', '9': '0oi8', '0': 'po9',
                'q': '12wa', 'w': '3esaq2', 'e': '4rdsw3', 'r': '5tfde4', 't': '6zgfr5', 'z': '7uhgt6', 'u': '8ijhz7', 'i': '9okju8', 'o': '0plki9', 'p': 'lo0',
                'a': 'qwsy', 's': 'edxyaw', 'd': 'rfcxse', 'f': 'tgvcdr', 'g': 'zhbvft', 'h': 'ujnbgz', 'j': 'ikmnhu', 'k': 'olmji', 'l': 'kop',
                'y': 'asx', 'x': 'ysdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhjm', 'm': 'njk'
                }
        azerty = {
                '1': '2a', '2': '3za1', '3': '4ez2', '4': '5re3', '5': '6tr4', '6': '7yt5', '7': '8uy6', '8': '9iu7', '9': '0oi8', '0': 'po9',
                'a': '2zq1', 'z': '3esqa2', 'e': '4rdsz3', 'r': '5tfde4', 't': '6ygfr5', 'y': '7uhgt6', 'u': '8ijhy7', 'i': '9okju8', 'o': '0plki9', 'p': 'lo0m',
                'q': 'zswa', 's': 'edxwqz', 'd': 'rfcxse', 'f': 'tgvcdr', 'g': 'yhbvft', 'h': 'ujnbgy', 'j': 'iknhu', 'k': 'olji', 'l': 'kopm', 'm': 'lp',
                'w': 'sxq', 'x': 'wsdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhj'
                }

        keyboards = [qwerty, qwertz, azerty]

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
                for keys in self.keyboards:
                    if self.word[i] in keys:
                        for c in keys[self.word[i]]:
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
                for keys in self.keyboards:
                    if self.word[i] in keys:
                        for c in keys[self.word[i]]:
                            result.append(self.word[:i] + c + self.word[i+1:])
            return result
        
        def transposition(self):
            result = []
            for i in range(0, len(self.word)-1):
                if self.word[i+1] != self.word[i]:
                    result.append(self.word[:i] + self.word[i+1] + self.word[i] + self.word[i+2:])
            return result

        def generate_words(self):
            possibilities=self.replacement()+self.bitsquatting()+self.vowel_swap()+self.add_on()+self.hyphenation()+self.insertion()+self.repetition()+self.transposition()
            #possibilities=self.transposition()
            res = []
            [res.append(x) for x in possibilities if x not in res]
            return res

    def __init__(self,url):
        r=tldextract.extract(url)
        self.subdomain=r.subdomain
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
            h1=self.Helper(self.subdomain)
            h2=self.Helper(self.subdomain)

            for protocol in self.Protocol:
                for subdomain in h2.generate_words():
                    for domain in h1.generate_words():
                        for tld in self.tlds:
                            results.append(protocol+'://'+subdomain+'.'+domain+'.'+tld+'/')'''

        h1=self.Helper(self.domain)

        for domain in h1.generate_words():
                #for tld in ["com"]:
                    #results.append(domain)
            results.append(domain)

        return results


url="www.google.com"
g=Domain_generator(url)
possible_urls=g.generate_urls()

with open('all.txt', 'w') as f:
    for item in possible_urls:
        s=f'{item}\n'
        f.write(s)