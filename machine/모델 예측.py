import torch

from transformers import BertTokenizer
from transformers import BertForSequenceClassification, AdamW, BertConfig
from transformers import get_linear_schedule_with_warmup
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

import pandas as pd
import numpy as np
import random
import time
import datetime
import re
import os
t = pd.read_table('train.txt', encoding='utf-8')

t['vader']=t['vader'].apply(pd.to_numeric,errors='coerce').fillna(2)
test=pd.DataFrame({'title':[],'label':[]})
i=0
for x in range(len(t)):
    if 0.9<float(t['vader'][x])<=1.0:
        test.loc[i,'title']=t['title'][x]
        test.loc[i,'label']=1
        i=i+1
for x in range(len(t)):
    if -1.0<=float(t['vader'][x])<-0.9:
        test.loc[i,'title']=t['title'][x]
        test.loc[i,'label']=2
        i=i+1
test['title'].nunique()
test.drop_duplicates(subset=['title'], inplace=True)
for x in range(len(test)):
    test['title'].iloc[x]=re.sub(r'[^a-zA-Z ]', '',str(test['title'].iloc[x]))
test['title'] = test['title'].str.replace('^ +', "")
test['title'].replace('', np.nan, inplace=True)





device = torch.device('cpu')
model=torch.load('homebitcoinmodel',map_location=device)




tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', do_lower_case=False)
# 입력 데이터 변환
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
        seq_mask = [float(i>0) for i in seq]
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





test=test.reset_index(drop=True)




result=pd.DataFrame({'title':[],'label':[]})
for x in range(int(len(test))):
    logits = test_sentences([test['title'][x]])
    result.loc[x,'title']=test['title'][x]
    if np.argmax(logits) == 1 :
        result.loc[x,'label']='pos'
        continue
    elif np.argmax(logits) == 0 :
        result.loc[x,'label']='neu'
        continue
    elif np.argmax(logits) == 2 :
        result.loc[x,'label']='neg'
        continue



result.to_csv('modelpredict2.csv')

