import pandas as pd
import os
def concat_csv(path, column_name):
    li = []
    for f in os.listdir(path):
        if f.endswith('.csv'):
            df = pd.read_csv(f"{path}/{f}",index_col = None, header=0)
            li.append(df)
    frame = pd.concat(li, axis = 0, ignore_index = True)
    frame = frame.drop_duplicates([column_name],keep='first') #중복 처리를 해준다.
    return frame

if __name__ == '__main__':
    subreddit = input("subreddit: ")
    is_title = input("is title?: (y/n) ")
    if is_title == 'Y' or is_title == 'y':
        path = f"../dataset/raw_data/title_data/{subreddit}/output"
        column_name = 'title'
    else:
        path = f"../dataset/raw_data/comment_data/{subreddit}/output"
        column_name = 'body'
    res = concat_csv(path,column_name)
    res = res.drop_duplicates([column_name],keep='first')
    res.to_csv(f'{path}/{subreddit}_train.csv',index=None)