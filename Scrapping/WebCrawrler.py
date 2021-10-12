import requests
import datetime
import numpy as np
import pandas as pd
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

article_title = []
article_link = []
article_media = []
article_date = []
dt = datetime.datetime.now()

for j in range(1, 20):#페이지
    print("j = ", j)

    url = "https://www.investing.com/news/cryptocurrency-news/{}".format(j)
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.select("div.largeTitle > article > div.textDiv")
    articles_detail = soup.select("div.largeTitle > article > div.textDiv .articleDetails .date")

    for i in range(len(articles)):
        article_title.append(articles[i].a.text) #제목
        if articles[i].a['href'][:5] == "https":
            article_link.append(articles[i].a['href']) #리다이렉트 링크?
        else:
            article_link.append(url + articles[i].a['href'])  #링크
        article_media.append(articles[i].span.text.split(' - ')[0][3:]) #매체

        if j<3:#날짜
            if articles_detail[i].text[3:].split(' ')[1][:6] == 'minute':
                article_date.append((dt - datetime.timedelta(minutes=int(articles_detail[i].text[3:].split(' ')[0]))).strftime("%b %d, %Y"))
            elif articles_detail[i].text[3:].split(' ')[1][:4] == 'hour':
                article_date.append((dt - datetime.timedelta(hours=int(articles_detail[i].text[3:].split(' ')[0]))).strftime("%b %d, %Y"))
            elif articles_detail[i].text[3:].split(' ')[0] == 'Just':
                article_date.append(dt.strftime("%b %d, %Y"))
            else:
                article_date.append(articles_detail[i].text[3:])
        else:
            article_date.append(articles_detail[i].text[3:])
        print("     i = ", i)

df = pd.DataFrame({"Title": article_title, "Link": article_link,
                   "Media": article_media, "Date": article_date})
df.to_csv('article.csv', index=False, encoding='UTF-8')
