import pandas as pd
import sys
import os
import re
import string
import spacy
import json
import operator

df = pd.read_csv('./data/twitter/cleaned.csv')
def get_sentiment(sentiment):
    if(sentiment == 'Positive'):
        return 1
    elif sentiment == 'Neutral':
        return 0
    else:
        return -1
df['sentiment'] = df['Final_Sentiment'].apply(get_sentiment)

df = df[['id', 'full_text', 'Text_clean', 'region', 'user','lib','cpc','ndp','sentiment']]

df_lib = df[df['lib'].isin([1])]
df_cpc = df[df['cpc'].isin([1])]
df_ndp = df[df['ndp'].isin([1])]

all_lib = df_lib[['lib', 'region']].groupby(['region']).count().reset_index()
all_con = df_cpc[['cpc', 'region']].groupby(['region']).count().reset_index()
all_ndp = df_ndp[['ndp', 'region']].groupby(['region']).count().reset_index()

lib_count = all_lib.to_dict('records')
con_count = all_con.to_dict('records')
ndp_count = all_ndp.to_dict('records')

def getHash(data, hashKey, valueKey):
    newData = {}
    for item in data:
        newData[item[hashKey]] = item[valueKey]
    return newData

lib_hash = getHash(lib_count, 'region', 'lib')
con_hash = getHash(con_count, 'region', 'cpc')
ndp_hash = getHash(ndp_count, 'region', 'ndp')

provinces = ['Alberta', 'Atlantic', 'British Columbia', 'Ontario', 'Praires', 'Quebec']
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

with open('./dashboard/public/static/tweets_map_mentions.json', 'w') as file:
    json.dump(all_data, file, indent=4, separators=(',', ': '))
