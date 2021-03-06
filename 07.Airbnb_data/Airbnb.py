# -*- coding: utf-8 -*-
"""FastCampus.ipynb

Automatically generated by Colaboratory.

This file needs to be run in 'https://colab.research.google.com/'. 
And AB_NYC_2019.csv must be uploaded in colab repository '/content/'
"""

import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


bnb = pd.read_csv('/content/AB_NYC_2019.csv')

bnb.head(3)

bnb.info()

print("총 데이터 개수: ", bnb.shape[0]*bnb.shape[1])
print("총 결측치 수: {} = 전체 데이터의 {:.2f}% ".format(bnb.isnull().sum().sum(), (bnb.isnull().sum().sum()*100)/(bnb.shape[0]*bnb.shape[1])))
print(f"계정의 개수 : {bnb['id'].nunique()}, 사용자의 수 : {bnb['name'].nunique()}")
print("호스트 ID: {} 개, 호스트 수 : {} 명".format(bnb['host_id'].nunique(), bnb['host_name'].nunique()))
print("2019년 뉴욕의 평균 Airbnb 금액 : {:.2f} $".format(bnb['price'].mean()))

bnb.isnull().sum()

import missingno #결측치 시각화 패키지 불러오기

missingno.matrix(bnb, figsize=(12, 5))

missingno.bar(bnb, figsize=(12, 5))

bnb.fillna({'review_per_month':0}, inplace = True)
bnb.fillna({'name':'NoName'}, inplace = True)

bnb.drop(['id','last_review'], axis=1, inplace=True)

bnb.duplicated().sum()
#bnb.drop_duplicates(inplace=True) #중복된 컬럼 존재시 삭제

bnb.describe()

len(bnb[bnb['price']==0])

f, ax = plt.subplots(1, 1, figsize=(8, 6))
sns.distplot(bnb['price'], hist=True, ax=ax)

ax.set_xlim(-500, 4000) #r값이 왼쪽에 몰려있으므로 x축 조정

print("( -3< skewness <3 이면 기준 충족) Skewness: %.2f" % bnb['price'].skew())
print(" 정규분포의 kurtosis = 0 이어야 함 )Kurtosis: %.2f" % bnb['price'].kurt ())

pd.concat([bnb['price'], bnb['minimum_nights']], axis=1)

bnb.plot.scatter(x='price', y='minimum_nights', ylim=(0, 1500), s=7, color='red')

f2, ax2 = plt.subplots(1, 1, figsize=(5, 6), dpi = 80)

sns.boxplot(data = bnb['price'], showfliers = True, ax=ax2)

f3, ax3 = plt.subplots(1, 1, figsize=(9, 8))

corrmat = bnb.corr()
sns.heatmap(data= corrmat, annot=True, cmap='YlGnBu', ax=ax3)
plt.title("Correlation map for Airbnb Data", size=15)

min_threshold, max_threshold = bnb['price'].quantile([0.01, 0.99])
min_threshold, max_threshold

print("기존 행 개수 : ", len(bnb['price']), "상위 1%, 하위 1%를 제외한 행의 개수 : ", len(bnb[(min_threshold < bnb['price']) & (bnb['price'] < max_threshold)]))

refined_bnb = bnb[(min_threshold < bnb['price']) & (bnb['price'] < max_threshold)]
refined_bnb.info()

sns.distplot(refined_bnb['price'])

print("( -3< skewness <3 이면 기준 충족) Skewness: %.2f" % refined_bnb['price'].skew())
print(" 정규분포의 kurtosis = 0 이어야 함 )Kurtosis: %.2f" % refined_bnb['price'].kurt ())

sns.boxplot(refined_bnb['price'])

top_host = refined_bnb.host_name.value_counts().head(15)
top_host

top_host_df = pd.DataFrame(top_host)
top_host_df.reset_index(inplace=True)
top_host_df.rename(columns={'index' : 'host_name', 'host_name' : 'count'}, inplace=True)
top_host_df

f4, ax4 = plt.subplots(1, 1, figsize=(12, 6))

sns.barplot(data=top_host_df, x='host_name', y='count', palette='rocket', ax=ax4)
ax4.set_title("NYCs top hosts with the most listings")
ax4.set_xlabel("Host Name")
ax4.set_ylabel("Count")

ax4.set_xticklabels(ax4.get_xticklabels(), rotation=30)

refined_bnb.groupby(['neighbourhood_group'])['price'].idxmax()  #가장 비싼 가격을 갖는 행의 인덱스 출력
refined_bnb.loc[refined_bnb.groupby(['neighbourhood_group'])['price'].idxmax()][['name', 'neighbourhood_group', 'host_name', 'price']]

refined_bnb.groupby(['neighbourhood_group'])['price'].idxmin()  #가장 싼 가격을 갖는 행의 인덱스 출력
refined_bnb.loc[refined_bnb.groupby(['neighbourhood_group'])['price'].idxmin()][['name', 'neighbourhood_group', 'host_name', 'price']]

refined_bnb['neighbourhood_group'].unique()

f5, ax5 = plt.subplots(1, 1, figsize = (12, 10))

sns.violinplot(data = refined_bnb,  x='neighbourhood_group', y='price', palette='winter', ax=ax5)
ax5.set_title("Prices with different regions")

refined_bnb['room_type'].unique()

room_type_df = refined_bnb.groupby(['neighbourhood_group'])['room_type'].value_counts().unstack(0)
room_type_df

graph = room_type_df.plot(kind='bar', figsize = (12, 6))
graph.set_title("Room types in various regions")
graph.set_xlabel("room_type", size = 15)
graph.set_ylabel("the number of rooms", size = 15)
graph.set_xticklabels(graph.get_xticklabels(), rotation = 0 , size=13)

hot10_review = refined_bnb.nlargest(10, "reviews_per_month")
hot10_review[['name', 'reviews_per_month', 'neighbourhood_group']]

f6, ax6 = plt.subplots(1, 1, figsize= (10, 8))

sns.stripplot(data = refined_bnb, x="room_type", y="reviews_per_month", hue = "neighbourhood_group", dodge=True, jitter= True, palette="Set2", ax=ax6)
#dodge : hue 별로 데이터를 나눠서 쌓아준다.
#jitter : 가로축 위치에 변동을 줘서 데이터가 겹치지 않게 해준다.

f7, ax7 = plt.subplots(1, 2, figsize = (18, 10))

sns.scatterplot(data=refined_bnb, x='longitude', y='latitude', hue='neighbourhood_group', palette='bright', edgecolor='black', linewidth=0.3, ax=ax7[0])
sns.scatterplot(data=refined_bnb, x='longitude', y='latitude', hue='room_type', palette="bright", edgecolor='black', linewidth=0.3, ax=ax7[1])

f8, ax8 = plt.subplots(1, 1, figsize=(10, 8))
#새로운 축으로서 크기를 추가하고 그 기준은 365일 중 이용가능한 일수!  
sns.scatterplot(data=refined_bnb, x='longitude', y='latitude', hue='availability_365', palette='coolwarm', size='availability_365', sizes=(20, 300))

#선형 회귀 분석 패키지 불러오기

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder

bnb_model = refined_bnb

#라벨인코더를 이용해 범주형 변수들을 더미 변수(임시 변수 ex>1, 2, 3, 4...)로 변환
labelencoder = LabelEncoder()
bnb_model['neighbourhood_group'] = labelencoder.fit_transform(bnb_model['neighbourhood_group'])
bnb_model['neighbourhood'] = labelencoder.fit_transform(bnb_model['neighbourhood'])
bnb_model['room_type'] = labelencoder.fit_transform(bnb_model['room_type'])

feature_columns = ['neighbourhood_group', 'neighbourhood', 'room_type', 'minimum_nights', 'calculated_host_listings_count', 'availability_365']

x = bnb_model[feature_columns]
y = bnb_model['price']

train_x, test_x, train_y, test_y = train_test_split(x, y, train_size=0.7, test_size=0.3, random_state = 42)
print(train_x.shape, test_x.shape, train_y.shape, test_y.shape)

linear_regression = LinearRegression()
linear_regression.fit(train_x, train_y)

print("(정확하게 예측하고 있는지 진단) Accuracy on test set : {}".format(round(linear_regression.score(test_x, test_y), 4)))

# 실제값과 예측값의 오차 확인
test_predict = linear_regression.predict(test_x)
compare = pd.DataFrame(np.array(test_y).flatten(), columns=['Actual'])
compare['Prediction'] = np.array(test_predict)
compare['Error'] = abs(compare['Actual'] - compare['Prediction'])
compare
