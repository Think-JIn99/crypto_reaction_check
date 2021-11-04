from pmaw import PushshiftAPI
import pandas as pd
import os.path
import datetime as dt
import typer
from dateutil.relativedelta import relativedelta
class API:
    def __init__(self, subreddit, start_point,end_point):
        self.api = PushshiftAPI()
        self.subreddit = subreddit
        self.start_point = dt.datetime.strptime(start_point,'%Y-%m-%d')
        self.end_point = dt.datetime.strptime(end_point,'%Y-%m-%d')

    def convert_to_df(self,submissions) -> pd.DataFrame:
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

    def extract_subreddit(self):
        _after = self.start_point
        end_point = self.end_point
        while _after <= end_point:
            _before = _after + relativedelta(months = 1)
            try:
                submissions = self.api.search_submissions(subreddit = self.subreddit, limit = 10000, before = int(_before.timestamp()), after = int(_after.timestamp()))
            except:
                continue
            submissions_df = self.convert_to_df(submissions)
            path = f'./dataset/{_after}.csv'
            if os.path.exists(path):
                submissions_df.to_csv(path, sep = ',', mode ='a', header = False, index = False)
            else:
                submissions_df.to_csv(path, sep=',',index = False)
            _after += relativedelta(months = 1)

            typer.echo(f"{self.subreddit}: {_after} ~ {_before}:  one epoch complete!!\n")
        

def main(subreddit:str, start_point:str, end_point:str):
    api = API(subreddit,start_point,end_point)
    if not os.path.exists(f'./dataset'):
        os.mkdir(f'./dataset')
    typer.echo(f"{api.subreddit}: {api.start_point} ~ {api.end_point} start scrapping")
    api.extract_subreddit()

if __name__ == '__main__':
    typer.run(main)
