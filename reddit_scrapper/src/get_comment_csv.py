from pmaw import PushshiftAPI  # 없으면 설치 해야해요 pip로 설치
import pandas as pd
import os
import datetime as dt
import typer  # 없으면 설치 해야해요 pip로 설치
#csv 읽어서 id값 받아오고
#extract_comments 돌리구 csv로


class API:
    def __init__(self, subreddit, start_point, end_point):
        self.api = PushshiftAPI()  # api 객체 생성
        self.subreddit = subreddit  # 갤러리 이름
        self.start_point = dt.datetime.strptime(start_point, '%Y-%m-%d')
        self.end_point = dt.datetime.strptime(end_point, '%Y-%m-%d')

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
        comment_ids = self.api.search_submission_comment_ids(ids=post_ids)  # post ids로 comment ids 받아옴
        comment_ids_list = [comment_ids for comment_ids in comment_ids]  # comment ids 리스트화
        comments = self.api.search_comments(ids=comment_ids_list)  # comment ids로 comments 받아옴
        comment_list = [comments for comments in comments]  # comments 리스트화
        comments_df = self.comments_to_df(comment_list)  # 데이터 프레임 형태로 변환
        if os.path.exists('./comment_data/f_name'):
            comments_df.to_csv('./comment_data/f_name', sep=',', mode='a', header=False, index=False)
        else:
            comments_df.to_csv('./comment_data/f_name', sep=',', index=False)

    def get_id(self):
        path = './filter_scrap_data/valid_data/'
        file_list = os.listdir(path)
        for f in file_list:
            print(f)
            df = pd.read_csv(f"{path}{f}")
            self.extract_comments(df.id, f)


def main(subreddit: str, start_point: str, end_point: str):
    api = API(subreddit, start_point, end_point)
    api.get_id()

if __name__ == '__main__':
    typer.run(main)

# python get_comment_csv.py Bitcoin 2020-01-01 2021-11-01
