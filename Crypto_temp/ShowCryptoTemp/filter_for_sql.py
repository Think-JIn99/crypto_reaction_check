import numpy as np
import re
from Crypto_temp.ShowCryptoTemp import create_regex


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
        #해당 패턴이 하나 이상 발견된 행들을 반환
        valid_index = np.where(patt_find.apply(len) > 0, True, False)
        res = res | valid_index
    return res

def get_valid_rows(df,column_name):
    pattern = create_regex.get_word_patt(False) #create_regex.py에 저장된 비트코인 연관 단어 패턴들을 가져온다.
    valid_index = find_pattern(df, pattern, column_name) #해당 단어가 포함된 글들은 유효하다.
    return df.loc[valid_index]

def remove_invalid_rows(df, column_name):
    patterns = create_regex.remove_patterns # 기본적으로 지워야할 url, nan등
    patterns.extend(create_regex.get_word_patt())# 광고 글에 자주 사용되는 단어들
    invalid_index = find_pattern(df, patterns, column_name) #삭제해야할 행 인덱스
    valid_df = df.loc[~invalid_index].copy()
    valid_df[column_name].replace(r"[^a-zA-Z ]","",regex = True, inplace=True) #이모지, 특수문자 제거
    valid_df[column_name].replace("", float("NaN"),inplace=True) #이모지로만 구성되거나 특수문자로만 구성됐던 글들 결측치로 변환
    valid_df.dropna(inplace = True) #결측치 전부 제거
    return valid_df

#메인 함수에 df를 넣어주면 실행됩니다.
#최종적으로 main에 남아있는 df가 필터를 전부 적용한 df입니다.
def filter_for_sql_main(df):
    try:
        column_name = 'title' # 처리할 열의 이름
        df = get_valid_rows(df,column_name)
        df = remove_invalid_rows(df, column_name)
        return df
    except Exception as e:
        print(e)