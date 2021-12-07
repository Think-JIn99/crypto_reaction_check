from django.http import HttpResponse
from django.shortcuts import render
from .models import *
import praw
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import re
import os
import torch
from transformers import BertTokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


def Praw(request):
    new_words = {
        'decline': -2.0,
        'declines': -2.0,
        'declined': -2.0,
        'incline': 2.0,
        'inclines': 2.0,
        'inclined': 2.0,
        'mainiac': 3.0,
        'moon': 4.0,
        'moons': 4.0,
        'high': 2.0,
        'slip': -1.0,
        'slipped': -1.0,
        'mooning': 4.0,
        'long': 2.0,
        'longs': 2.0,
        'short': -2.0,
        'shorts': -2.0,
        'lose': -2.0,
        'loss': -2.0,
        'lost': -2.0,
        'volatile': -2.0,
        'volatiles': -2.0,
        'weak': -2.0,
        'weaken': -2.0,
        'strong': 2.0,
        'fall': -2.0,
        'fallen': -2.0,
        'falls': -2.0,
        'fell': -2.0,
        'doom': -3.0,
        'climb': 2.0,
        'climbs': 2.0,
        'climbed': 2.0,
        'climbing': 2.0,
        'tumble': -2.0,
        'tumbles': -2.0,
        'tumbled': -2.0,
        'tumbling': -2.0,
        'fear': -2.0,
        'plunge': -2.0,
        'recession': -2.0,
        'plunges': -2.0,
        'plunged': -2.0,
        'inches': 2.0,
        'record': 2.0,
        'ralie': 2.0,
        'ralies': 2.0,
        'ralied': 2.0,
        'above': 2.0,
        'aboves': 2.0,
        'hit': 1.3,
        'hits': 1.3,
        'hitting': 1.3,
        'hodl': 2.0,
        'ATH': 3.0,
        'call': 2.0,
        'dip': -2.0,
        'ponzi': -3.0,
        'break': 2.0,
        'breaks': 2.0,
        'tendie': 2.0,
        'surge': 2.0,
        'surges': 2.0,
        'surged': 2.0,
        'overvalue': -3.0,
        'overvalued': -3.0,
        'rise': 2.0,
        'soar': 2.0,
        'soars': 2.0,
        'soared': 2.0,
        'undervalue': 2.0,
        'undervalued': 2.0,
        'buy the dip': 2.5,
        'buy': 4.0,
        'bought': 4.0,
        'buying': 4.0,
        'sell': -4.0,
        'selling': -4.0,
        'sold': -4.0,
        'paper': -1.5,
        'bagholder': -1.5,
        'hold': 1.5,
        'holds': 1.5,
        'holding': 1.5,
        'top': 2.0,
        'tops': 2.0,
        'topped': 2.0,
        'hack': -2.0,
        'hacked': -2.0,
        'hacks': -2.0,
        'hacking': -2.0,
        'stonk': 1.5,
        'scam': -3.0,
        'scams': -3.0,
        'scammed': -3.0,
        'scamming': -3.0,
        'profit': 2.0,
        'profits': -2.0,
        'green': 2,
        'red': -2,
        'money': 1.5,
        'print': 1.5,
        'sky': 1.5,
        'rocket': 3.2,
        'rockets': 3.2,
        'rocketed': 3.2,
        'bull': 3,
        'bear': -3,
        'pump': 2.0,
        'pumps': 2.0,
        'pumping': 2.0,
        'pumped': 2.0,
        'offering': -1,
        'rip': -2.0,
        'downgrade': -2.0,
        'downgrades': -2.0,
        'downgraded': -2.0,
        'dump': -2.0,
        'dumped': -2.0,
        'dumps': -2.0,
        'dumping': -2.0,
        'upgrade': 2.0,
        'upgraded': 2.0,
        'upgrades': -2.0,
        'hot': 1.5,
        'drop': -2.5,
        'dropped': -2.5,
        'rebound': 1.5,
        'rebounds': 1.5,
        'rebounded': 1.5,
        'up': 2.0,
        'down': -2.0,
        'downs': -2.0,
        'downed': -2.0,
        'crash': -2.5,
        'crack': -2.5,
        'cracks': -2.5,
        'cracked': -2.5,
        'disaster': -3.0,
    }

    def get_vader_df(df, column_name):
        analyzer = SentimentIntensityAnalyzer()  # vader 객체
        analyzer.lexicon.update(new_words)
        title_vader = df[column_name].apply(analyzer.polarity_scores)
        # df로 변환해 반환해준다.
        vader_title_df = pd.DataFrame(dict(title_vader)).T
        return vader_title_df  # vader실행 결과를 반환해준다.

    remove_words = [
        'free',
        'install',
        'download',
        'app',
        'wallet',
        'hardware',
        'link',
        'card',
        'payapl',
        'mine',
        'platform',
        'browser',
        'site',
        'earn',
        'project',
        'check'
    ]

    include_words = [
        'price', 'crypto',
        'currency', 'money',
        'BTC', 'bitcoin', 'bit',
        'ETH', 'ether', 'ethereum',
        'XRP', 'ripple',
        'DOGE', 'doge',
        'coin', 'market', 'elon', 'musk',
        'fed', 'powell'
    ]
    url_patt = r"(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}"
    nan_patt = r"(^.?removed.?$)|(^.?deleted.?$)"  # 결측치 제거용
    remove_patterns = [url_patt, nan_patt]

    def get_word_patt(is_remove=True):
        if is_remove:
            words = remove_words
        else:
            include_words.extend(new_words.keys())
            words = include_words
        word_patt = [r"\b" + w + r"+(\w{1,3})?\b" for w in words]
        word_patt = "|".join(word_patt)
        return [word_patt]

    def find_pattern(df, patterns, column_name):
        valid_index = [True] * df.shape[0]
        res = [False] * df.shape[0]
        for patt in patterns:
            patt_find = df[column_name].str.findall(patt, flags=re.IGNORECASE)
            # 해당 패턴이 하나 이상 발견된 행들을 반환
            valid_index = np.where(patt_find.apply(len) > 0, True, False)
            res = res | valid_index
        return res

    def get_valid_rows(df, column_name):
        pattern = get_word_patt(False)  # create_regex.py에 저장된 비트코인 연관 단어 패턴들을 가져온다.
        valid_index = find_pattern(df, pattern, column_name)  # 해당 단어가 포함된 글들은 유효하다.
        return df.loc[valid_index]

    def remove_invalid_rows(df, column_name):
        patterns = remove_patterns  # 기본적으로 지워야할 url, nan등
        patterns.extend(get_word_patt())  # 광고 글에 자주 사용되는 단어들
        invalid_index = find_pattern(df, patterns, column_name)  # 삭제해야할 행 인덱스
        valid_df = df.loc[~invalid_index].copy()
        valid_df[column_name].replace(r"[^a-zA-Z ]", "", regex=True, inplace=True)  # 이모지, 특수문자 제거
        valid_df[column_name].replace("", float("NaN"), inplace=True)  # 이모지로만 구성되거나 특수문자로만 구성됐던 글들 결측치로 변환
        valid_df.dropna(inplace=True)  # 결측치 전부 제거
        return valid_df

    # 메인 함수에 df를 넣어주면 실행됩니다.
    # 최종적으로 main에 남아있는 df가 필터를 전부 적용한 df입니다.
    def filter_for_sql_main(df):
        try:
            column_name = 'title'  # 처리할 열의 이름
            df = get_valid_rows(df, column_name)
            df = remove_invalid_rows(df, column_name)
            return df
        except Exception as e:
            print(e)

    reddit = praw.Reddit(
        client_id="_i0Z1_b3Xs0LGPdfGqt3JQ",
        client_secret="iplaFZ16URV1GQVtBpAaWaCg9V51pA",
        user_agent="CryptoScrap by /u/LunarJun",
    )

    device = torch.device('cpu')
    model = torch.load('/Users/jihunlee/Projects/crypto_reaction_check/Crypto_temp/ShowCryptoTemp/bitcoinmodel05',
                       map_location=device)
    tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', do_lower_case=False)

    def convert_input_data(sentences):
        sentences = ["[CLS] " + str(sentence) + " [SEP]" for sentence in sentences]
        # BERT의 토크나이저로 문장을 토큰으로 분리
        tokenized_texts = [tokenizer.tokenize(sent) for sent in sentences]

        # 입력 토큰의 최대 시퀀스 길이
        MAX_LEN = 128

        # 토큰을 숫자 인덱스로 변환
        input_ids = [tokenizer.convert_tokens_to_ids(x) for x in tokenized_texts]

        # 문장을 MAX_LEN 길이에 맞게 자르고, 모자란 부분을 패딩 0으로 채움
        input_ids = pad_sequences(input_ids, maxlen=MAX_LEN, dtype="long", truncating="post", padding="post")

        # 어텐션 마스크 초기화
        attention_masks = []

        # 어텐션 마스크를 패딩이 아니면 1, 패딩이면 0으로 설정
        # 패딩 부분은 BERT 모델에서 어텐션을 수행하지 않아 속도 향상
        for seq in input_ids:
            seq_mask = [float(i > 0) for i in seq]
            attention_masks.append(seq_mask)

        # 데이터를 파이토치의 텐서로 변환
        inputs = torch.tensor(input_ids).to(torch.int64)
        masks = torch.tensor(attention_masks).to(torch.int64)

        return inputs, masks

    # 문장 테스트
    def test_sentences(sentences):

        # 평가모드로 변경
        model.eval()

        # 문장을 입력 데이터로 변환
        inputs, masks = convert_input_data(sentences)

        # 데이터를 GPU에 넣음
        b_input_ids = inputs.to(device)
        b_input_mask = masks.to(device)

        # 그래디언트 계산 안함
        with torch.no_grad():
            # Forward 수행
            outputs = model(b_input_ids,
                            token_type_ids=None,
                            attention_mask=b_input_mask)

        # 로스 구함
        logits = outputs[0]

        # CPU로 데이터 이동
        logits = logits.detach().cpu().numpy()

        return logits

    def ModelPredict(df):
        for x in range(1, int(len(df))):
            if df['title'][x]:
                logits = test_sentences([df['title'][x]])  # 이 부분을 바꾸시면 됩니다 해당 dataframe으로
                if np.argmax(logits) == 1:
                    df.loc[x, 'predict_value'] = 1  # 이 부분을 바꾸시면 됩니다 해당 dataframe으로
                    continue
                elif np.argmax(logits) == 0:
                    df.loc[x, 'predict_value'] = 0  # 이 부분을 바꾸시면 됩니다 해당 dataframe으로
                    continue
                elif np.argmax(logits) == 2:
                    df.loc[x, 'predict_value'] = -1  # 이 부분을 바꾸시면 됩니다 해당 dataframe으로
                    continue

        return df

    def submission_to_df(submission) -> pd.DataFrame:
        data = {'post_id': [submission.id],
                'title': [submission.title],
                'created_utc': [submission.created_utc]}
        df = pd.DataFrame(data)
        return df[::][::]

    subreddit = reddit.subreddit("Bitcoin")
    submissions_dataframe = pd.DataFrame()
    submissions_df = pd.DataFrame(columns=['post_id', 'title', 'created_utc', 'predict_value'])
    for submission in subreddit.new(limit=100):
        submissions_dataframe = submissions_dataframe.append(submission_to_df(submission))
    submissions_dataframe = filter_for_sql_main(submissions_dataframe)
    submissions_df = pd.concat([submissions_df, submissions_dataframe], ignore_index=True)
    submissions_df['predict_value'] = 0
    submissions_df = ModelPredict(submissions_df)
    df = submissions_df.values.tolist()
    # logit_test = test_sentences((["El Salvador Bought  Bitcoins In The Dip"]))
    print(submissions_df)
    listdf = []
    for row in df:
        listdf.append(scrapper(post_id=row[0],
                               title=row[1],
                               created_utc=row[2],
                               predict_value=row[3]
                               ))

    scrapper.objects.bulk_create(listdf)

    # scrapper_df_to_model = scrapper()
    # scrapper_df_to_model.myList = json.dumps(df)
    # scrapper_df_to_model.save()

    return HttpResponse("success")


def index(request):
    Bitcoin_temp_Query = ShowCryptoTemp.objects.filter(CryptoName='BitCoin')
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
    return render(request, "ShowCryptoTemp/about.html", context)
