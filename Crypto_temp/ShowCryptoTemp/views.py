from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *
from pmaw import PushshiftAPI  # 없으면 설치 해야해요 pip로 설치
import pandas as pd
import os.path
import datetime as dt
import typer  # 없으면 설치 해야해요 pip로 설치
import sqlite3
from dateutil.relativedelta import relativedelta




def index(request):
    Bitcoin_temp_Query = ShowCryptoTemp.objects.filter(CryptoName= 'BitCoin')
    Ethereum_temp_Query = ShowCryptoTemp.objects.filter(CryptoName='Ethereum')
    Doge_temp_Query = ShowCryptoTemp.objects.filter(CryptoName='Doge')
    AdA_temp_Query = ShowCryptoTemp.objects.filter(CryptoName='ADA')
    Ripple_temp_Query = ShowCryptoTemp.objects.filter(CryptoName='Ripple')

    Bitcoin_temp = float(Bitcoin_temp_Query.values('CryptoTemperture')[0]['CryptoTemperture'])
    Ethereum_temp = float(Ethereum_temp_Query.values('CryptoTemperture')[0]['CryptoTemperture'])
    Doge_temp = float(Doge_temp_Query.values('CryptoTemperture')[0]['CryptoTemperture'])
    AdA_temp = float(AdA_temp_Query.values('CryptoTemperture')[0]['CryptoTemperture'])
    Ripple_temp = float(Ripple_temp_Query.values('CryptoTemperture')[0]['CryptoTemperture'])


    context = {
        'Bitcoin_temp': Bitcoin_temp,
        'Ethereum_temp': Ethereum_temp,
        'Doge_temp': Doge_temp,
        'AdA_temp': AdA_temp,
        'Ripple_temp': Ripple_temp,
    }
    # return HttpResponse(Bitcoin_temp)
    return render(request,"ShowCryptoTemp/about.html",context)

def PandasToDjango(request):
    class API:
        def __init__(self, subreddit):
            self.api = PushshiftAPI()  # api 객체 생성
            self.subreddit = subreddit  # 갤러리 이름
            # self.con = sqlite3.connect("ShowCryptoTemp_showcryptotemp")  # db 파일 연결

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

        def extract_subreddit(self):
            now = dt.datetime.now().strftime('%Y-%m-%d')
            before = now - relativedelta(hours=1)

            try:
                # 업로드된 게시글을 최대 10000개 가져온다.
                submissions = self.api.search_submissions(subreddit=self.subreddit, limit=10000,
                                                          before=int(now.timestamp()),
                                                          after=int(before.timestamp()))
            except:
                pass
            submissions_df = self.submissions_to_df(submissions)  # 데이터 프레임 형태로 변환
            submissions_df.rename(columns={'id': 'post_id'}, inplace=True)  # 장고에 id가 기본으로 쓰이므로 post_id로 수정
            typer.echo(f"{self.subreddit}: {now} ~ {before}:  one epoch complete!!\n")
            # post_ids = submissions_df['post_id']  # post ids 추출
            # self.extract_comments(post_ids, now)  # post ids로 comments 받아옴

            return submissions_df[::]

    subreddit = "Bitcoin"
    api = API(subreddit)
    data = api.extract_subreddit()
    context = {
        'df': data,
            }

    return HttpResponse(data)