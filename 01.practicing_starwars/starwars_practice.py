# -*- coding: utf-8 -*-
"""
Automatically generated by Colaboratory.

This code need to be run in 'https://colab.research.google.com/' and upload starwars.csv in colab repository '/content/'
"""

import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.rc('font', family='NanumBarunGothic')

plt.style.use('seaborn')
sns.set(font_scale=1)

sw = pd.read_csv('/content/Starwars.csv')
print(sw.head())
print('\n', sw.shape)
print('총 데이터 개수', sw.shape[0]*sw.shape[1])
print('총 결측치 수: {} = 전체 데이터의 {:.2f}%'.format(sw.isnull().sum().sum(), (sw.isnull().sum().sum()*100)/(sw.shape[0]*sw.shape[1])))
print('스타워즈에 등장하는 등장인물 수:', sw['name'].nunique())
print('스타워즈에 등장하는 종족 수:', sw['species'].nunique())

f, ax = plt.subplots(1, 2, figsize=(18, 8))

sw['gender'].value_counts().plot.pie(ax=ax[0], autopct = '%1.0f%%', shadow=True)
ax[0].set_title('Starwars: Gender', size=18)
ax[0].set_ylabel('')

sns.countplot(data=sw, y='sex', ax=ax[1])
ax[1].set_title('Starwars: Sex', size=18)

plt.show()

print('Skewness: %f' % sw['height'].skew())
print('Kurtosis: %f' % sw['height'].kurt())

f2, ax2 = plt.subplots(1,2, figsize=(18, 8))

sns.distplot(sw[sw['sex'] == 'male']['height'],  ax=ax2[0])
sns.distplot(sw[sw['sex'] == 'female']['height'], ax=ax2[0])
sns.distplot(sw[sw['sex'] == 'robot']['height'], ax=ax2[0])
ax2[0].legend(['male', 'female', 'robot'])

sns.kdeplot(sw[sw['gender'] == 'masculine']['height'], ax=ax2[1])
sns.kdeplot(sw[sw['gender'] == 'feminine']['height'], ax=ax2[1])
ax2[1].legend(['masculine', 'feminine'])

weight = sw[['species', 'mass']].groupby(['species'], as_index=True).mean()

f3, ax3 = plt.subplots(1,1, figsize=(10, 8))

colors=sns.color_palette('hls', len(weight['mass']))

g = weight['mass'].sort_values(ascending = False).plot.bar(color=colors)
g.set_xticklabels(g.get_xticklabels(), rotation=77)

plt.show()

out1 = sw['species'].isin(['Hutt'])
out2 = sw['mass'].isin([np.nan]) 

sw[-out1][-out2].shape 

sns.lmplot(data=sw[-out1][-out2], x='height', y='mass')
sns.set_style(style='darkgrid')

plt.show()
