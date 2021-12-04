import numpy as np
import pandas as pd
import re
import typer
import os
from apply_vader import get_vader_df #vader 값 적용해주는 함수
from remove_word import get_word_patt
def pre_process(raw_df, column_name):
    if "selftext" in raw_df.columns: #제목의 경우 결측치가 많아 제거해 사용합니다.
        raw_df.drop('selftext',axis=1,inplace=True)
    df = raw_df.dropna() #여백 및 결측치를 제거해준다.
    df = df.drop_duplicates([column_name],keep='first') #중복 처리를 해준다.
    return df

def remove_pattern(df, patterns, column_name):
 #   valid_index = [True] * df.shape[0] 인댁싱을 위한 불리언 배열
    res = [True] * df.shape[0]
    for patt in patterns:
        patt_find = df[column_name].str.findall(patt, flags = re.IGNORECASE)
        valid_index = np.where(patt_find.apply(len) == 0, True, False)
        res = res & valid_index
    return res #삭제하지 말아야할 배열의 인덱스들

def get_valid_df(df, column_name):
    patterns =  get_word_patt() #remove_words.py에 저장된 삭제할 패턴들을 가져온다.
    valid_index = remove_pattern(df, patterns, column_name) #광고글 삭제 진행
    return df.loc[valid_index] #광고가 아닌 글로 판정된 글들 df형태로 반환
    
def main(subreddit:str, is_title:str):
    #터미널에서 실행할 때 사용하는 부분
    if is_title == 'Y' or is_title == 'y':
        path = f'../dataset/raw_data/title_data/{subreddit}'
        column_name = 'title'
    else:
        path = f'../dataset/raw_data/comment_data/{subreddit}'
        column_name = 'body'
    for f in os.listdir(path):
        try:
            df = pre_process(pd.read_csv(f"{path}/{f}"), column_name)
            typer.echo(f"{f}: start processing") #터미널 출력 문구
            total_cnt = df.shape[0] #삭제한 글의 수를 파악하기 위해 사용
            df = get_valid_df(df, column_name)
            #문자 형태의 데이터만 남긴다.
            df[column_name].replace(r"[^a-zA-Z ]","",regex = True, inplace=True) #모델에서 이모지나 특수문자를 처리 못하기 때문에 추가적으로 삭제
            df[column_name].replace("", float("NaN"),inplace=True) #이모지나 특수기호로만 이뤄진 글을 결측치로 만들어준다.
            df = df.dropna() #이모지로만 구성됐던 글들을 전부 제거한다.
            df['vader'] = get_vader_df(df, column_name)['compound'] #vader 실행
            removed_cnt = total_cnt - df.shape[0]
            out_path = f'{path}/output'
            #파일 작성
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
