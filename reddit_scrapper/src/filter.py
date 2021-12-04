import numpy as np
import pandas as pd
import re
import typer
import os
from apply_vader import get_vader_df #명령어 subreddit title,comment 여부 입력으로 실행
from remove_word import get_word_patt
def pre_process(raw_df, column_name):
    if "selftext" in raw_df.columns:
        raw_df.drop('selftext',axis=1,inplace=True)
    df = raw_df.dropna() #여백 및 결측치를 제거해준다.
    df = df.drop_duplicates([column_name],keep='first') #중복 처리를 해준다.
    return df

def remove_pattern(df, patterns, column_name):
    valid_index = [True] * df.shape[0]
    res = [True] * df.shape[0]
    for patt in patterns:
        patt_find = df[column_name].str.findall(patt, flags = re.IGNORECASE)
        valid_index = np.where(patt_find.apply(len) == 0, True, False)
        res = res & valid_index
    return res

def get_valid_df(df, column_name):
    patterns =  get_word_patt()
    valid_index = remove_pattern(df, patterns, column_name)
    return df.loc[valid_index]
    
def main(subreddit:str, is_title:str):
    if is_title == 'Y' or is_title == 'y':
        path = f'../dataset/raw_data/title_data/{subreddit}'
        column_name = 'title'
    else:
        path = f'../dataset/raw_data/comment_data/{subreddit}'
        column_name = 'body'
    for f in os.listdir(path):
        try:
            df = pre_process(pd.read_csv(f"{path}/{f}"), column_name)
            typer.echo(f"{f}: start processing")
            total_cnt = df.shape[0]
            df = get_valid_df(df, column_name)
            #문자 형태의 데이터만 남긴다.
            df[column_name].replace(r"[^a-zA-Z ]","",regex = True, inplace=True)
            df[column_name].replace("", float("NaN"),inplace=True)
            df = df.dropna() #이모지로만 구성됐던 글들을 전부 제거한다.
            df['vader'] = get_vader_df(df, column_name)['compound']
            removed_cnt = total_cnt - df.shape[0]
            out_path = f'{path}/output'
            if not os.path.exists(out_path):
                    os.mkdir(f'{out_path}')
            df.to_csv(f"{out_path}/{f}",index=False)
            typer.echo(f"{f}: end processing (total: {total_cnt} removed: {removed_cnt})")
        except Exception as e:
            typer.echo(f"{f} has problem")
            typer.echo(e)
            continue
        
if __name__ == '__main__':
    typer.run(main)
