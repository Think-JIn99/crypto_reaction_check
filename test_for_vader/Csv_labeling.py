import pandas as pd
import math
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

new_words = {
    'citron': -4.0,
    'hidenburg': -4.0,
    'moon': 4.0,
    'highs': 2.0,
    'mooning': 4.0,
    'long': 2.0,
    'short': -2.0,
    'call': 4.0,
    'calls': 4.0,
    'put': -4.0,
    'puts': -4.0,
    'break': 2.0,
    'tendie': 2.0,
     'tendies': 2.0,
     'town': 2.0,
     'overvalued': -3.0,
     'undervalued': 3.0,
     'buy': 4.0,
     'sell': -4.0,
     'gone': -1.0,
     'gtfo': -1.7,
     'paper': -1.7,
     'bullish': 3.7,
     'bearish': -3.7,
     'bagholder': -1.7,
     'stonk': 1.9,
     'green': 1.9,
     'money': 1.2,
     'print': 2.2,
     'rocket': 2.2,
     'bull': 2.9,
     'bear': -2.9,
     'pumping': -1.0,
     'sus': -3.0,
     'offering': -2.3,
     'rip': -4.0,
     'downgrade': -3.0,
     'upgrade': 3.0,
     'maintain': 1.0,
     'pump': 1.9,
     'hot': 1.5,
     'drop': -2.5,
     'rebound': 1.5,
     'crack': 2.5,}

portion_count = [0]*10  #구간 카운트
vader = {'title_vader': [], 'selftext_vader': []}   #vader 결과
df_list = []                                        #csv에서 추출된 친구들

analyzer = SentimentIntensityAnalyzer()
analyzer.lexicon.update(new_words)

for k in range(1,9):#부족하면 다음 csv파일로
    df = pd.read_csv("../reddit_scrapper/src/dataset/2020-0{}-01 00_00_00.csv".format(str(k)))
    for i in df.iloc:
        vs = analyzer.polarity_scores(i.title)['compound']
        a = math.floor(float(vs)*5 + 4) #0.2 구간의 인덱스화
        if portion_count[a] < 100:  #각 구간 count가 100미만인지
            portion_count[a] = portion_count[a]+1
            vader['title_vader'].append(float(vs))
            df_list.append(i.values.tolist())
            if ((i.selftext == "[deleted]") | (i.selftext == "[removed]")) & (type(i.selftext) is str):#selftext가 [deleted], [removed]
                vader['selftext_vader'].append('x')
                continue
            if i.selftext == '':        #selftext가 공백인 경우
                vader['selftext_vader'].append('x')
                continue
            vs = analyzer.polarity_scores(str(i))['compound']
            vader['selftext_vader'].append(float(vs))

    if portion_count[9] == 100:     #일반적으로 가장 수가 적은 0.8~1이 100이 되었는지 확인
        break


df2 = pd.concat([pd.DataFrame(df_list, columns= ['id','author','title','selftext','created_utc','num_comments','score']),
                 pd.DataFrame(vader)], axis=1)
df2.to_csv('output.csv', index=False, encoding='UTF-8')
