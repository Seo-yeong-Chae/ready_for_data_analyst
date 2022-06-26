# -*- coding: utf-8 -*-
"""FastCampus.ipynb

Automatically generated by Colaboratory.

this file needs to be run in 'https://colab.research.google.com/'. 
And 'US Superstore data.xls' must be uploaded in colab repository '/content/'

"""

import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.style.use('seaborn')
sns.set(font_scale=1)


!pip install --upgrade xlrd
#업그레이드가 적용되려면 이 코드 실행 후 런타임 다시 시작해야 함

sp=pd.read_excel('/content/US Superstore data.xls')

sp.head(5)

sp.info()

sp.describe()

sp.describe(include=np.object)

print("총 데이터 수: ", sp.shape[0]*sp.shape[1])
print("총 결측치 수: {} = 전체 데이터의 {:.2f} % ".format(sp.isnull().sum().sum(), (sp.isnull().sum().sum())*100/(sp.shape[0]*sp.shape[1])) )
print("판매 기간: {} ~ {}".format(min(sp['Order Date']), max(sp['Order Date'])))
print("전체 판매 물건 종류: {} 개".format(sp['Product ID'].nunique()))

sp.duplicated().sum()

sp.columns

sp1 = sp.drop(['Postal Code'], axis=1)
sp1.columns = ['row_id', 'order_id', 'order_date', 'ship_date', 'ship_mode', 'cust_id', 'cust_name', 'seg', 'country', 'city', 'state', 'region', 'product_id', 'category', 'sub-category',
       'product_name', 'sales', 'quantity', 'discount', 'profit']

sp1.columns

sp1['product_id'].value_counts().head(10)

f, ax = plt.subplots(1, 2, figsize=(13, 10))

sns.violinplot(x=sp1['category'], y=sp1['sales'], ax=ax[0])
sns.violinplot(x=sp1['category'], y=sp1['discount']*100, ax=ax[1])

plt.figure(figsize=(12, 10))
sp1['sub-category'].value_counts().plot.pie(autopct="%1.1f%%")

plt.show()

top_states = sp1['state'].value_counts().nlargest(10)
top_states

f2, ax2 = plt.subplots(1, 1, figsize=(25, 8))

g = sns.countplot(sp1["state"].sort_values(), ax=ax2) 
g.set_xticklabels(g.get_xticklabels(), rotation=90)
g.set_title("Sales per state", size=15)
g.set_ylabel('')

plt.show()

f3, ax3 = plt.subplots(1, 2, figsize=(14, 9))

sns.countplot(x=sp1['seg'], palette='magma', ax=ax3[0])
ax3[0].set_title('Segment', size=16)

sns.countplot(x=sp1['region'], palette='magma', ax=ax3[1])
ax3[1].set_title('Region', fontsize=16)

plt.show()

f4, ax4 = plt.subplots(1, 1, figsize=(10, 6))

sns.lineplot(data=sp1, x='discount', y='profit', color='red', ax=ax4)

ax4.set_xlabel('Discount (%)')
ax4.set_ylabel('profit (%)')

plt.show()

sp_corr = sp1[['sales','quantity', 'discount', 'profit']].corr()
sp_corr

f5, ax5 = plt.subplots(1, 1, figsize=(9, 8))
sns.heatmap(data = sp_corr, annot=True, cmap='YlGnBu', ax=ax5)
plt.title("Sales, Quantity, Discount and Profit's correlation", size=16)

top_item=sp1.groupby(['product_name']).sum().sort_values('sales', ascending=False).head(10)
top_item

top_item.reset_index(inplace=True)
top_item

f6, ax6 = plt.subplots(1, 1, figsize=(9, 8))

ax6.pie(top_item['sales'], labels=top_item['product_name'], autopct="%1.1f%%", startangle=0)
ax6.set_ylabel('')

sales = sp1.groupby(['state']).sum().sort_values('sales', ascending=False)
sales.reset_index(inplace=True)
sales

dc = sales[sales['state'] == 'District of Columbia'].index
sales = sales.drop(dc)
sales.reset_index(inplace=True)

sales.drop('index', 1, inplace=True)
sales

sales['state'].unique()

state = ['California', 'New York', 'Texas', 'Washington', 'Pennsylvania',
       'Florida', 'Illinois', 'Ohio', 'Michigan', 'Virginia',
       'North Carolina', 'Indiana', 'Georgia', 'Kentucky', 'New Jersey',
       'Arizona', 'Wisconsin', 'Colorado', 'Tennessee', 'Minnesota',
       'Massachusetts', 'Delaware', 'Maryland', 'Rhode Island',
       'Missouri', 'Oklahoma', 'Alabama', 'Oregon', 'Nevada',
       'Connecticut', 'Arkansas', 'Utah', 'Mississippi', 'Louisiana',
       'Vermont', 'South Carolina', 'Nebraska', 'New Hampshire',
       'Montana', 'New Mexico', 'Iowa', 'Idaho', 'Kansas', 'Wyoming',
       'South Dakota', 'Maine', 'West Virginia', 'North Dakota']

state_code = ['CA', 'NY', 'TX', 'WA', 'PA',
       'FL', 'IL', 'OH', 'MI', 'VA',
       'NC', 'IN', 'GA', 'KY', 'NJ',
       'AZ', 'WI', 'CO', 'TN', 'MN',
       'MA', 'DE', 'MD', 'RI',
       'MO', 'OK', 'AL', 'OR', 'NV',
       'CT', 'AR', 'UT', 'MS', 'LA',
       'VT', 'SC', 'NE', 'NH',
       'MT', 'NM', 'IA', 'ID', 'KS', 'WY',
       'SD', 'ME', 'WV', 'ND']
state_cd = pd.DataFrame(state, state_code)
state_cd.reset_index(inplace=True)
state_cd.columns=['state_code', 'state']
state_cd

sales.insert(1, 'state_code', state_cd['state_code'])
sales=sales.sort_values('state', ascending=True)

sales.reset_index(inplace=True)

sales.drop('index', 1, inplace=True)
sales

import plotly.express as px

fig = px.choropleth(locations=sales['state_code'], locationmode='USA-states', color=sales['sales'], scope='usa', color_continuous_scale='peach', title='gmv per state in USA')

fig.show()