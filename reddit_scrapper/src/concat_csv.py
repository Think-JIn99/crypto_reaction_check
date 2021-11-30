import pandas as pd
import os
def concat_csv(subreddit, path):
    li = []
    for f in os.listdir(path):
        df = pd.read_csv(f"{path}/{f}",index_col = None, header=0)
        li.append(df)
    frame = pd.concat(li, axis = 0, ignore_index = True)
    return frame

if __name__ == '__main__':
    subreddit = input("subreddit: ")
    is_title = input("is title?: (y/n) ")
    if is_title == 'Y' or is_title == 'y':
        path = f"../dataset/title_data/{subreddit}"
    else:
        path = f"../dataset/comment_data/{subreddit}"
    res = concat_csv(subreddit, path)
    res.to_csv(f'{path}/_train.csv',index=None)
    