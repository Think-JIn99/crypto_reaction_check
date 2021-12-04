from pmaw import PushshiftAPI  # 없으면 설치 해야해요 pip로 설치
import pandas as pd
import os
import datetime as dt
import typer  # 없으면 설치 해야해요 pip로 설치
import time
from dateutil.relativedelta import relativedelta


class API:
    def __init__(self):
        self.api = PushshiftAPI()  # api 객체 생성

    def comments_to_df(self, submissions) -> pd.DataFrame:
        # 추출할 속성들
        columns = [
            'id',
            'body',
            'created_utc',
            'score',
            'link_id',
            'parent_id',
        ]
        df = pd.DataFrame(submissions)
        return df[::][columns]

    def extract_comments(self, post_ids, f_name):  # try except 넣어야할지 고민중
        _before = dt.datetime.strptime(f_name.rstrip('.csv'), '%Y-%m-%d')
        _after = _before + relativedelta(months=1)

        start = time.time()
        comment_ids = self.api.search_submission_comment_ids(ids=post_ids, limit=10000, subreddit='Bitcoin',
                                                             _before=_before,
                                                             _after=_after)  # post ids로 comment ids 받아옴
        comment_ids_list = [comment_ids for comment_ids in comment_ids]  # comment ids 리스트화
        print("time :", time.time() - start)

        start = time.time()
        comments = self.api.search_comments(ids=comment_ids_list, subreddit='Bitcoin',
                                            limit=10000, _before=_before,
                                            _after=_after)  # comment ids로 comments 받아옴
        comment_list = [comments for comments in comments]  # comments 리스트화
        print("time :", time.time() - start)

        comments_df = self.comments_to_df(comment_list)  # 데이터 프레임 형태로 변환
        path = f'./filter_scrap_data/comment_data/{f_name}'
        print(path)
        if os.path.exists(path):
            comments_df.to_csv(path, sep=',', mode='a', header=False, index=False)
        else:
            comments_df.to_csv(path, sep=',', index=False)

    def get_id(self):
        path = './filter_scrap_data/valid_data/'
        file_list = os.listdir(path)
        for f in file_list:
            print(f)
            if f in os.listdir('./filter_scrap_data/comment_data/'):
                print('pass')
                continue
            else:
                df = pd.read_csv(f"{path}{f}")
                self.extract_comments(df.id, f)


def main():
    api = API()
    api.get_id()

if __name__ == '__main__':
    typer.run(main)

# python get_comment_csv.py
