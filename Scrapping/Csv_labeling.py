import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

vader_label = []
analyzer = SentimentIntensityAnalyzer()
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
