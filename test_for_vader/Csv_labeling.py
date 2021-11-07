import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

vader_label = []

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

analyzer = SentimentIntensityAnalyzer()
analyzer.lexicon.update(new_words)
df = pd.read_csv("comments.csv")

for i in df['body']:
    vs = analyzer.polarity_scores(str(i))['compound']
    if float(vs) >= 0.3:
        vader_label.append('1')
    elif vs <= -0.3:
        vader_label.append('-1')
    else:
        vader_label.append('0')

df['vader'] = vader_label
df.to_csv('output.csv', index=False, encoding='UTF-8')
