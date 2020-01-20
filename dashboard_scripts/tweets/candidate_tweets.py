import pandas as pd
import spacy
import sys
import os
import operator
import re
import json
import numpy as np

sp = spacy.load('en_core_web_sm') 
df = pd.read_csv('./data/twitter/cleaned.csv')
parties_tag_df = df[['id', 'Final_Sentiment','Final_Sentiment_Probability', 'lib', 'cpc', 'ndp']]

def get_sentiment(sentiment):
    if(sentiment == 'Positive'):
        return 1
    elif sentiment == 'Neutral':
        return 0
    else:
        return -1
parties_tag_df['sentiment'] = parties_tag_df['Final_Sentiment'].apply(get_sentiment)

df_lib = parties_tag_df[parties_tag_df['lib'].isin([1])]
df_cpc = parties_tag_df[parties_tag_df['cpc'].isin([1])]
df_ndp = parties_tag_df[parties_tag_df['ndp'].isin([1])]

candidates = {}

def getPercentage(data, party):
    sentiment_count = data[['id', 'sentiment']].groupby(['sentiment']).count().reset_index()
    data_count = len(data)
    sentiment_count['percentage'] = sentiment_count.apply(lambda x : 100 * x['id'] / float(data_count), axis=1)
    result = sentiment_count.to_dict('records')
    for i in result:
        if i['sentiment'] == 1.0:
            candidates[party+'Positive'] = round(i['percentage'],1)
        if i['sentiment'] == 0.0:
            candidates[party+'Neutral'] = round(i['percentage'],1)
        if i['sentiment'] == -1.0:
            candidates[party+'Negative'] = round(i['percentage'],1)

getPercentage(df_lib, 'lpc')
getPercentage(df_cpc, 'cpc')
getPercentage(df_ndp, 'ndp')

with open('./dashboard/public/static/candidateTweets.json', 'w') as file:
    json.dump(candidates, file, indent=4, separators=(',', ': '))