import praw
import pandas as pd
import datetime as dt
from praw.models import MoreComments


class Praw:
    def __init__(self):  # 매개변수 subreddit 추가 가능
        subreddit = 'Bitcoin'
        self.now = dt.datetime.now()
        self.reddit = self.praw_connect()
        self.subreddit = self.praw_connect().subreddit(subreddit)  # 갤러리 이름
        # self.con = sqlite3.connect("ShowCryptoTemp_showcryptotemp")   # db 파일 연결

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

    def utc_30min(self, now, then):
        min_diff = (now - dt.datetime.fromtimestamp(then)).seconds / 60
        print(int(min_diff))
        if int(min_diff) < 30:
            return True
        else:
            return False

    def extract_sub_comt(self):
        submissions_df = pd.DataFrame()
        comments_df = pd.DataFrame()
        for submission in self.subreddit.new(limit=20):
            if not self.utc_30min(self.now, submission.created_utc):
                continue
            submissions_df = submissions_df.append(self.submission_to_df(submission))
            for comment in submission.comments:
                if isinstance(comment, MoreComments):
                    continue
                comments_df = comments_df.append(self.comment_to_df(comment))

        print(submissions_df)
        print(comments_df)


scrapper = Praw()
scrapper.extract_sub_comt()
