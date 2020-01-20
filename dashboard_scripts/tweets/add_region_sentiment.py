import pandas as pd
import sys
import os
import re
import string
import spacy
import json

df = pd.read_csv('./data/twitter/cleaned.csv')
# df = pd.read_csv('./Data/Twitter/region-tags.csv', index_col=None, header=0)
def get_sentiment(sentiment):
    if(sentiment == 'Positive'):
        return 1
    elif sentiment == 'Neutral':
        return 0
    else:
        return -1
df['sentiment'] = df['Final_Sentiment'].apply(get_sentiment)

df = df[['id', 'full_text', 'Text_clean', 'region', 'user','lib','cpc','ndp','sentiment']]
df['Sentiment5'] = df['sentiment'].apply(lambda x : x*5)

df_lib = df[df['lib'].isin([1])]
df_cpc = df[df['cpc'].isin([1])]
df_ndp = df[df['ndp'].isin([1])]

provinces = ['Alberta', 'Atlantic', 'British Columbia', 'Ontario', 'Praires', 'Quebec']

all_lib = df_lib[['region', 'Sentiment5']].groupby(['region']).mean().reset_index()
all_con = df_cpc[['region', 'Sentiment5']].groupby(['region']).mean().reset_index()
all_ndp = df_ndp[['region', 'Sentiment5']].groupby(['region']).mean().reset_index()

lib_count = all_lib.to_dict('records')
con_count = all_con.to_dict('records')
ndp_count = all_ndp.to_dict('records')


def getHash(data, hashKey, valueKey):
    newData = {}
    for item in data:
        newData[item[hashKey]] = item[valueKey]
    return newData

lib_hash = getHash(lib_count, 'region', 'Sentiment5')
con_hash = getHash(con_count, 'region', 'Sentiment5')
ndp_hash = getHash(ndp_count, 'region', 'Sentiment5')
all_data = []

for province in provinces:
    maxi = ''
    if con_hash[province] > lib_hash[province]:
        if con_hash[province] > ndp_hash[province]:
            maxi = 'Conservative'
        else:
            maxi = 'NDP'
    else:
        if lib_hash[province] > ndp_hash[province]:
            maxi = 'Liberals'
        else:
            maxi = 'NDP'

    item = {}
    
    item['Province'] = province
    item['Conservative'] = con_hash[province]
    item['NDP'] = ndp_hash[province]
    item['Liberals'] = lib_hash[province]
    item['Max'] = maxi
    all_data.append(item)

with open('./dashboard/public/static/tweets_map_sentiment.json', 'w') as file:
    json.dump(all_data, file, indent=4, separators=(',', ': '))