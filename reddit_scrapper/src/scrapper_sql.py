from pmaw import PushshiftAPI  # 없으면 설치 해야해요 pip로 설치
import pandas as pd
import os.path
import datetime as dt
import typer  # 없으면 설치 해야해요 pip로 설치
import sqlite3
from dateutil.relativedelta import relativedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

new_words = {
    'citron': -4.0,
    'hidenburg': -4.0,
    'moon': 4.0,
    'highs': 2.0,
    'mooning': 4.0,
    'long': 2.0,
    'short': -2.0,
    'call': 4.0,
    'calls': 4.0,
    'put': -4.0,
    'puts': -4.0,
    'break': 2.0,
    'tendie': 2.0,
    'tendies': 2.0,
    'town': 2.0,
    'overvalued': -3.0,
    'undervalued': 3.0,
    'buy': 4.0,
    'sell': -4.0,
    'gone': -1.0,
    'gtfo': -1.7,
    'paper': -1.7,
    'bullish': 3.7,
    'bearish': -3.7,
    'bagholder': -1.7,
    'stonk': 1.9,
    'green': 1.9,
    'money': 1.2,
    'print': 2.2,
    'rocket': 2.2,
    'bull': 2.9,
    'bear': -2.9,
    'pumping': -1.0,
    'sus': -3.0,
    'offering': -2.3,
    'rip': -4.0,
    'downgrade': -3.0,
    'upgrade': 3.0,
    'maintain': 1.0,
    'pump': 1.9,
    'hot': 1.5,
    'drop': -2.5,
    'rebound': 1.5,
    'crack': 2.5,}

class API:
    def __init__(self, subreddit, start_point, end_point):
        self.api = PushshiftAPI()  # api 객체 생성
        self.subreddit = subreddit  # 갤러리 이름
        self.start_point = dt.datetime.strptime(start_point, '%Y-%m-%d')
        self.end_point = dt.datetime.strptime(end_point, '%Y-%m-%d')
        self.con = sqlite3.connect("test.db")   # db 파일 연결

    def submissions_to_df(self, submissions) -> pd.DataFrame:
        # 추출할 속성들
        columns = [
            'id',
            'author',
            'title',
            'selftext',
            'created_utc',
            'num_comments',
            'score',
        ]
        df = pd.DataFrame(submissions)
        return df[::][columns]

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

    def extract_comments(self, post_ids, _after):   # try except 넣어야할지 고민중
        comment_ids = self.api.search_submission_comment_ids(ids=post_ids)  # post ids로 comment ids 받아옴
        comment_ids_list = [comment_ids for comment_ids in comment_ids] # comment ids 리스트화
        comments = self.api.search_comments(ids=comment_ids_list)   # comment ids로 comments 받아옴
        comment_list = [comments for comments in comments]  # comments 리스트화
        comments_df = self.comments_to_df(comment_list)  # 데이터 프레임 형태로 변환
        # vader열을 만들어 vader의 compound값 입력
        comments_df['vader'] = self.get_vader_df(comments_df['body'])['compound']
        comments_df.to_sql(_after.strftime("comment"),
                           con=self.con, if_exists='append', chunksize=1000, method='multi')

    def extract_subreddit(self):
        _after = self.start_point  # 시작점을 의미 합니다. 이 시점부터 긁어옴
        end_point = self.end_point  # 끝점을 의미 합니다. 이 시점까지 긁어옴
        while _after < end_point:
            _before = _after + relativedelta(hours=4)  # 긁을 간격을 정하여 _before를 잡아준다.
            try:
                # 업로드된 게시글을 최대 10000개 가져온다.
                submissions = self.api.search_submissions(subreddit=self.subreddit, limit=10000,
                                                          before=int(_before.timestamp()),
                                                          after=int(_after.timestamp()))
            except:
                continue
            submissions_df = self.submissions_to_df(submissions)  # 데이터 프레임 형태로 변환
            # vader열을 만들어 vader의 compound값 입력
            submissions_df['vader'] = self.get_vader_df(submissions_df['title'])['compound']
            submissions_df.to_sql(_after.strftime("submission"),
                                  con=self.con, if_exists='append', chunksize=4000, method='multi')

            # 콘솔에 진행상황 출력
            typer.echo(f"{self.subreddit}: {_after} ~ {_before}:  one epoch complete!!\n")

            post_ids = submissions_df['id']  # post ids 추출
            self.extract_comments(post_ids, _after)  # post ids로 comments 받아옴

            # 시작점을 간격만큼 미뤄준다.
            _after += relativedelta(hours=4)

    def get_vader_df(self, df):
        analyzer = SentimentIntensityAnalyzer()
        analyzer.lexicon.update(new_words)
        vader = df.dropna().apply(analyzer.polarity_scores)
        # df로 변환해 반환해준다.
        vader_df = pd.DataFrame(dict(vader)).T
        return vader_df  # vader실행 결과를 반환해준다.


def main(subreddit: str, start_point: str, end_point: str):
    # 스크래퍼 객체 생성
    api = API(subreddit, start_point, end_point)
    if not os.path.exists(f'./dataset'):
        os.mkdir(f'./dataset')
    typer.echo(f"{api.subreddit}: {api.start_point} ~ {api.end_point} start scrapping")
    api.extract_subreddit()
    api.con.close()


if __name__ == '__main__':
    typer.run(main)
# python scrapper_sql.py Bitcoin 2021-11-01 2021-11-02
