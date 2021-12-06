import numpy as np
import pandas as pd
import re
import typer
import os
from apply_vader import get_vader_df #명령어 subreddit title,comment 여부 입력으로 실행
import create_regex
def pre_process(raw_df, column_name):
    if "selftext" in raw_df.columns: #제목의 경우 결측치가 많아 제거해 사용합니다.
        raw_df.drop('selftext',axis=1,inplace=True)
    df = raw_df.dropna() #여백 및 결측치를 제거해준다.
    df = df.drop_duplicates([column_name],keep='first') #중복 처리를 해준다.
    return df

def find_pattern(df, patterns, column_name):
    valid_index = [True] * df.shape[0]
    res = [False] * df.shape[0]
    for patt in patterns:
        patt_find = df[column_name].str.findall(patt, flags = re.IGNORECASE)
        valid_index = np.where(patt_find.apply(len) > 0, True, False)
        res = res | valid_index
    return res #삭제하지 말아야할 인덱스

def get_valid_row(df,column_name):
    pattern = create_regex.get_word_patt(False) #create_regex.py에 저장된 비트코인 연관 단어 패턴들을 가져온다.
    valid_index = find_pattern(df, pattern, column_name) #해당 단어가 포함된 글들은 유효하다.
    return df.loc[valid_index]

def do_remove(df, column_name):
    patterns =  create_regex.get_word_patt()
    patterns.append(create_regex.nan_patt)#nan 찾는 패턴
    patterns.append(create_regex.url_patt)#url 탐지 패턴
    valid_index = find_pattern(df, patterns, column_name) #삭제해야할 행 인덱스
    return df.loc[~valid_index] #삭제
    
def main(subreddit:str, is_title:str):
    #터미널에서 실행할 때 사용하는 부분
    if is_title == 'Y' or is_title == 'y':
        path = f'../dataset/raw_data/title_data/{subreddit}'
        column_name = 'title'
    else:
        path = f'../dataset/raw_data/comment_data/{subreddit}'
        column_name = 'body'
    for f in os.listdir(path):
        if f.endswith('.csv'): # csv형태로 끝나는 파일만.
            try:
                df = pre_process(pd.read_csv(f"{path}/{f}"), column_name)
                typer.echo(f"{f}: start processing")
                total_cnt = df.shape[0]
                df = get_valid_row(df,column_name)
                df = do_remove(df, column_name)
                #문자 형태의 데이터만 남긴다.
                df[column_name].replace(r"[^a-zA-Z ]","",regex = True, inplace=True)
                df[column_name].replace("", float("NaN"),inplace=True) #공백 글 결측치로 치환
                df = df.dropna() #공백 글들을 전부 제거한다.
                df['vader'] = get_vader_df(df, column_name)['compound'] #베이더 적용
                removed_cnt = total_cnt - df.shape[0] #삭제한 글의 수 확인을 위해 사용
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
