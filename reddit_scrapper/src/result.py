import pandas as pd
import datetime as dt


df = pd.read_csv("./filter_scrap_data/valid_data/concat_csv.ipynb/total.csv")
df2 = pd.DataFrame({'period': [], 'pos': [], 'neg': []})  # period별 결과값을 넣을 dataframe

for i in df.iloc:  # 행마다 반복
    now = dt.datetime.now()  # 일단 하루단위
    min_diff = (now - dt.datetime.fromtimestamp(i.created_utc)).total_seconds() / 60 / 60 / 24
    if (df2['period'] == int(min_diff)).any():
        if i.title_vader > 0.5:     # title_vader 모델결과로 바꾸면됨
            df2.loc[(df2['period'] == int(min_diff)), 'pos'] += 1
        elif i.title_vader < -0.5:
            df2.loc[(df2['period'] == int(min_diff)), 'neg'] += 1
    else:
        df2 = df2.append({'period': int(min_diff), 'pos': 0, 'neg': 0}, ignore_index=True)

df2 = df2.sort_values(by='period', ascending=True)  # 최근부터 오름차순 정렬
df2 = df2.set_index('period')   # index period로

df2['axis'] = df2['pos']/(df2['pos'] + df2['neg'])*100  # 그냥 비율
data_std = (df2['axis'] - df2['axis'].min()) / (df2['axis'].max() - df2['axis'].min())  # 정규화
df2['axis'] -= 20   # 평균이 70정도라 20빼줌    기간이 짧으면 0 이하로 튈수 있음

print(df2['axis'].min())
print(df2['axis'].mean())
print(df2['axis'].max())

print(data_std.min())
print(data_std.mean())
print(data_std.max())

# 저장부분 구현하면 될듯
# 저장은 df2['axis'] 혹은 data_std한 정규화 data
# 어떤거 쓸지는 아직 모르겠음
# print 신경쓰이면 지워도 됨
'''
그래프 그리는 부분
mov5 = df2['axis'].rolling(5).mean()
mov10 = df2['axis'].rolling(10).mean()
plt.plot(df2['axis'])
plt.plot(mov5)
plt.plot(mov10)
plt.show()
'''
