import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os 
from vader_feature import new_words
def get_vader_df(df):
    #결측치 인덱스를 걸러낸다.
    title_valid_index = df.index[(df['title'] != '[removed]') & (df['title'] != '[deleted]')].tolist()
    self_valid_index = df.index[(df['selftext'] != '[removed]') & (df['selftext'] != '[deleted]')].tolist()
    #결측치가 아닌 행들을 df 형태로 구축한다.
    title_for_vader = df['title'].loc[title_valid_index]
    self_for_vader = df['selftext'].loc[self_valid_index]
    
    #removed 나 deleted가 아닌 공백이나 NAN 등의 경우를 마저 없애주고 vader를 실행한다.
    title_vader = title_for_vader.dropna().apply(analyzer.polarity_scores)
    self_vader = self_for_vader.dropna().apply(analyzer.polarity_scores)
    
    #df로 변환해 반환해준다.
    vader_title_df = pd.DataFrame(dict(title_vader)).T
    vader_self_df = pd.DataFrame(dict(self_vader)).T

    return vader_title_df, vader_self_df

def extract_sample(vader_df,sample_indexes):
    sample_size = 100
    for i in range(10):
        ticks = 0.1 * i #0.1을 간격으로 추출한다.
        compound = vader_df['compound']
        sample_set = vader_df.loc[(ticks <= compound) & (compound < (ticks + 0.1))]
        if sample_set.size > sample_size:
            #표본 크기 만큼 랜덤 추출한다.
            sample = sample_set.sample(n=sample_size,random_state=1004)
        else:
            sample = sample_set.sample(frac=1,random_state=1004)
        sample_indexes = np.append(sample_indexes, sample.index.values)
    return sample_indexes


def print_df(df,vader_self_df,vader_title_df,sample_indexes):
    #샘플 중 하나라도 값을 가지고 있다면 df에 출력해준다.
    df = df[['id','author','title_vader','title','self_vader','selftext','created_utc','num_comments','score']]
    return df.loc[list(sample_indexes)]


if __name__ == '__main__':
    path = '../reddit_scrapper/src/dataset/'
    file_list = os.listdir(path)                                       
    analyzer = SentimentIntensityAnalyzer() #vader 객체
    analyzer.lexicon.update(new_words)
    output = pd.DataFrame({})
    for f in file_list:
        df = pd.read_csv(f"{path}{f}")
        try:
            vader_title_df ,vader_self_df = get_vader_df(df)
            #df에 vader결과 추가
            df['self_vader'] = vader_self_df['compound']
            df['title_vader'] = vader_title_df['compound']
            sample_indexes = np.array([])
            #샘플 데이터의 인덱스 추출
            sample_indexes = extract_sample(vader_title_df,sample_indexes)
            sample_indexes = extract_sample(vader_self_df,sample_indexes)
            output = print_df(df,vader_title_df,vader_self_df,sample_indexes)
            if os.path.exists('./output.csv'):
                output.to_csv('./output.csv',sep=',',mode='a',index=False,header=False)
            else:
                output.to_csv("./output.csv",sep=',')
            print(f'{f} is completed')
        except:
            print('got some problem')
            continue