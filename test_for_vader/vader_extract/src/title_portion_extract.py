import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os 
from vader_feature import new_words
def get_vader_df(df):
    title_vader = df['title'].dropna().apply(analyzer.polarity_scores)
    #df로 변환해 반환해준다.
    vader_title_df = pd.DataFrame(dict(title_vader)).T
    return vader_title_df #vader실행 결과를 반환해준다.

def extract_sample(vader_df):
    sample_size = 100 #추출할 표본의 크기
    sample_df = pd.DataFrame({})
    for i in range(-10,11,1): # -1 ~ 1까지
        ticks = i / 10 #0.1씩 증가한다.
        compound = vader_df['title_vader']
        sample_set = vader_df.loc[(ticks <= compound) & (compound < (ticks + 0.1))]
        if len(sample_set) > sample_size:
            sample = sample_set.sample(n=sample_size,random_state=1004)
        else:
            sample = sample_set.sample(frac=1)
        sample_df = pd.concat([sample_df,sample])
    return sample_df

def print_df(sample_df):
    #컬럼 순서 재정렬
    sample_df = sample_df[['id','author','title_vader','title','selftext','created_utc','num_comments','score']]
    #행 별로 중복을 제거해준다.
    output = sample_df.drop_duplicates(subset = None, keep='first', ignore_index = False)
    #csv 파일을 작성해준다.
    if os.path.exists('./output/title_output.csv'):
        output.to_csv('./output/title_output.csv',sep=',',mode='a',index=False,header=False)
    else:
        output.to_csv("./output/title_output.csv",sep=',',index=False)
    print(f'{f} is completed')
    return 

if __name__ == '__main__':
    path = '../../reddit_scrapper/dataset/'
    file_list = os.listdir(path)                                       
    analyzer = SentimentIntensityAnalyzer() #vader 객체
    analyzer.lexicon.update(new_words)
    output = pd.DataFrame({})
    for f in file_list:
        df = pd.read_csv(f"{path}{f}")
        try:
            vader_title_df = get_vader_df(df)
            df['title_vader'] = vader_title_df['compound']
            sample_df = extract_sample(df)
            print_df(sample_df)
        except Exception as e:
            print(f'{e} got some problem')
            continue