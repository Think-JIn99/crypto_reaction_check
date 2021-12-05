from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *
import json
from pmaw import PushshiftAPI  # 없으면 설치 해야해요 pip로 설치
import praw
import pandas as pd
import datetime as dt
import typer
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

def Praw(request):
    reddit = praw.Reddit(
        client_id="_i0Z1_b3Xs0LGPdfGqt3JQ",
        client_secret="iplaFZ16URV1GQVtBpAaWaCg9V51pA",
        user_agent="CryptoScrap by /u/LunarJun",
    )

    def submission_to_df(submission) -> pd.DataFrame:
        df = pd.DataFrame({'post_id': [submission.id],
                           'title': [submission.title],
                           'created_utc': [submission.created_utc]})
        return df[::][::]

    subreddit = reddit.subreddit("Bitcoin")
    submissions_df = pd.DataFrame()
    for submission in subreddit.new(limit=100):
        submissions_df = submissions_df.append(submission_to_df(submission))

    df = submissions_df.values.tolist()
    listdf = []
    for row in df:
        listdf.append(scrapper(post_id = row[0],
                 title = row[1],
                 created_utc = row[2]
                 ))

    scrapper.objects.bulk_create(listdf)

    # scrapper_df_to_model = scrapper()
    # scrapper_df_to_model.myList = json.dumps(df)
    # scrapper_df_to_model.save()

    return HttpResponse("success")