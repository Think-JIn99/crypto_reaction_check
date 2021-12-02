import numpy as np
import pandas as pd
import re
import typer
import os
from apply_vader import get_vader_df #명령어 subreddit title,comment 여부 입력으로 실행
from remove_word import get_word_patt
def read_file(path):
    df = pd.read_csv(path)
    if "selftext" in df.columns:
        df.drop('selftext',axis=1,inplace=True)
    df = df.drop_duplicates(['title'],keep='first') #중복 처리를 해준다.
    df['title'] = df['title'].replace(r"[^a-zA-Z ]",'',regex=True)#문자 형태의 데이터만 남긴다.
    df.dropna(subset=['title'], inplace=True) #여백 및 결측치를 제거해준다.
    return df

def remove_pattern(df, patterns, column_name):
    valid_index = [True] * df.shape[0]
    res = [True] * df.shape[0]
    for patt in patterns:
        patt_find = df[column_name].str.findall(patt, flags = re.IGNORECASE)
        valid_index = np.where(patt_find.apply(len) == 0, True, False)
        res = res & valid_index
    return res

    
def get_valid_df(df):
    column_name = 'title'
    patterns =  get_word_patt()
    valid_index = remove_pattern(df, patterns, column_name)
    return df.loc[valid_index]

def main(subreddit:str, is_title:str):
    if is_title == 'Y' or is_title == 'y':
        path = f'../dataset/raw_data/title_data/{subreddit}'
    else:
        path = f'../dataset/raw_data/comment_data/{subreddit}'
    if not os.path.exists(path):
        os.mkdir(path)
    for f in os.listdir(path):
        try:
            df = read_file(f"{path}/{f}")
            typer.echo(f"{f}: start processing")
            total_cnt = df.shape[0]
            df = get_valid_df(df)
            df['vader'] = get_vader_df(df)['compound']
            removed_cnt = total_cnt - df.shape[0]
            df = df[['id','author','vader','title','created_utc','num_comments','score']]
            df.to_csv(f'{path}/{f}')
            typer.echo(f"{f}: end processing (total: {total_cnt} removed: {removed_cnt})")
        except Exception as e:
            typer.echo(e)
            continue
        
if __name__ == '__main__':
    typer.run(main)
