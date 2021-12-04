from vader_feature import new_words
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
analyzer = SentimentIntensityAnalyzer() #vader 객체
analyzer.lexicon.update(new_words)
def get_vader_df(df, column_name):
    title_vader = df[column_name].dropna().apply(analyzer.polarity_scores)
    #df로 변환해 반환해준다.
    vader_title_df = pd.DataFrame(dict(title_vader)).T
    return vader_title_df #vader실행 결과를 반환해준다.


