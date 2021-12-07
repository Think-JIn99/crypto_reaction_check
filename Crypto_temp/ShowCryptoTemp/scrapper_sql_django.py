import praw
import pandas as pd
import datetime as dt
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from praw.models import MoreComments

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
    'crack': 2.5
}


class Praw:
    def __init__(self):  # 매개변수 subreddit 추가 가능
        subreddit = 'Bitcoin'
        self.now = dt.datetime.now()
        self.reddit = self.praw_connect()
        self.subreddit = self.praw_connect().subreddit(subreddit)  # 갤러리 이름
        self.con = sqlite3.connect("ShowCryptoTemp_showcryptotemp")  # db 파일 연결

    def praw_connect(self):
        reddit = praw.Reddit(
            client_id="_i0Z1_b3Xs0LGPdfGqt3JQ",
            client_secret="iplaFZ16URV1GQVtBpAaWaCg9V51pA",
            user_agent="CryptoScrap by /u/LunarJun")
        if reddit.read_only:
            return reddit

    def submission_to_df(self, submission) -> pd.DataFrame:
        df = pd.DataFrame({'id': [submission.id],
                           'title': [submission.title],
                           'created_utc': [submission.created_utc]})
        return df[::][::]

    def comment_to_df(self, comment) -> pd.DataFrame:
        df = pd.DataFrame({'body': [comment.body],
                           'submission': [comment.submission],
                           'created_utc': [comment.created_utc], })
        return df[::][::]

    def utc_60min(self, now, then):
        min_diff = (now - dt.datetime.fromtimestamp(then)).seconds / 60
        print(int(min_diff))
        if int(min_diff) < 60:
            return True
        else:
            return False

    def get_vader_df(self, df):
        analyzer = SentimentIntensityAnalyzer()
        analyzer.lexicon.update(new_words)
        vader = df.dropna().apply(analyzer.polarity_scores)
        # df로 변환해 반환해준다.
        vader_df = pd.DataFrame(dict(vader)).T
        return vader_df  # vader실행 결과를 반환해준다.

    def extract_sub_comt(self):
        submissions_df = pd.DataFrame()
        comments_df = pd.DataFrame()
        for submission in self.subreddit.new(limit=20):
            if not self.utc_60min(self.now, submission.created_utc):
                continue
            submissions_df = submissions_df.append(self.submission_to_df(submission))
            for comment in submission.comments:
                if isinstance(comment, MoreComments):
                    continue
                comments_df = comments_df.append(self.comment_to_df(comment))

        print(submissions_df)
        print(comments_df)

        submissions_df['vader'] = self.get_vader_df(submissions_df['title'])['compound']
        submissions_df.rename(columns={'id': 'post_id'}, inplace=True)  # 장고에 id가 기본으로 쓰이므로 post_id로 수정
        submissions_df.to_sql("submission",
                              con=self.con, if_exists='append', chunksize=4000, method='multi')

        comments_df['vader'] = self.get_vader_df(comments_df['body'])['compound']
        comments_df.to_sql("comment",
                           con=self.con, if_exists='append', chunksize=1000, method='multi')


if __name__ == '__main__':
    scrapper = Praw()
    scrapper.extract_sub_comt()
    scrapper.con.close()
