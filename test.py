import requests
import re
from bs4 import BeautifulSoup

# url = 'https://www.google.com/search?q=digitalocean%2520www%2520DigitalOcean+%7C+The+Cloud+for+Builders&sxsrf=ALiCzsaqxOr2MBNmG7GITqhp0eS6CuzVMw%3A1670224550579&source=hp&ei=ppqNY6uRIfLpmAX3j4HICg&iflsig=AJiK0e8AAAAAY42otrWqrLt4NHySkjMFqWiNh_7uxA-I&ved=0ahUKEwir_J6o9-H7AhXyNKYKHfdHAKkQ4dUDCAg&uact=5&oq=digitalocean%2520www%2520DigitalOcean+%7C+The+Cloud+for+Builders&gs_lcp=Cgdnd3Mtd2l6EANQAFgAYOUBaABwAHgAgAEAiAEAkgEAmAEAoAECoAEB&sclient=gws-wiz'
# reqs = requests.get(url)
# soup = BeautifulSoup(reqs.text, 'html.parser')
 
# urls = []
# for link in soup.find_all('a'):
#     print(link.get('href'))

# from googlesearch import search   
# query = "digital ocean"
# links = []
# for j in search(query, num_results = 5): 
#     print("Link:", j)
#     links.append(j) 

# from googlesearch import search   

# # to search 
# query = "Geeksforgeeks"

# links = []
# for j in search(query, tld="co.in", num=10, stop=10, pause=2): 
#     links.append(j) 

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36' 
}

page = requests.get(f"https://www.bing.com/search?q=icdcit&first=30",headers=headers,timeout=3)
print(f"Search link: www.bing.com/search?q=digital?")
soup = BeautifulSoup(page.content,"lxml")
links = soup.find_all("cite")
# links = soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)"))

print()