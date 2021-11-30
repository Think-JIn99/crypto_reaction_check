from os import path
from pmaw import PushshiftAPI #없으면 설치 해야해요 pip로 설치
import pandas as pd
import os.path
import datetime as dt
import typer #없으면 설치 해야해요 pip로 설치
from dateutil.relativedelta import relativedelta
class API:
    def __init__(self, subreddit, start_point,end_point):
        self.api = PushshiftAPI() # api 객체 생성
        self.subreddit = subreddit # 갤러리 이름
        self.start_point = dt.datetime.strptime(start_point,'%Y-%m-%d')
        self.end_point = dt.datetime.strptime(end_point,'%Y-%m-%d')

    def convert_to_df(self,submissions) -> pd.DataFrame:
        #추출할 속성들
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

    def extract_subreddit(self,path):
        _after = self.start_point #시작점을 의미 합니다. 이 시점 이후로 긁어옴
        end_point = self.end_point #끝점을 의미 합니다. 여기까지 긁는 것이 목표
        while _after <= end_point:
            _before = _after + relativedelta(months = 1) # 한달 간격으로 데이터를 읽으므로 한달 뒤를 기준으로 잡아준다.
            try:
                #최대 한달동안 업로드된 게시글을 최대 10000개 가져온다. 
                submissions = self.api.search_submissions(subreddit = self.subreddit, limit = 10000, before = int(_before.timestamp()), after = int(_after.timestamp()))
            except:
                continue
            submissions_df = self.convert_to_df(submissions) #데이터 프레임 형태로 변환
            file_name = f'{path}/{_after}.csv'
            #데이터 프레임을 csv 파일로 작성한다.
            if os.path.exists(file_name):
                submissions_df.to_csv(file_name, sep = ',', mode ='a', header = False, index = False)
            else:
                submissions_df.to_csv(file_name, sep=',',index = False)
            #시작점을 한달 뒤로 미뤄준다.
            _after += relativedelta(months = 1)

            #콘솔에 진행상황 출력
            typer.echo(f"{self.subreddit}: {_after} ~ {_before}:  one epoch complete!!\n")
        

def main(subreddit:str, start_point:str, end_point:str):
    #스크래퍼 객체 생성
    api = API(subreddit,start_point,end_point)
    path = f'../dataset/title_dataset/{subreddit}'
    if not os.path.exists(path):
        os.mkdir(f'{path}')
    typer.echo(f"{api.subreddit}: {api.start_point} ~ {api.end_point} start scrapping")
    api.extract_subreddit(path)

if __name__ == '__main__':
    typer.run(main)
