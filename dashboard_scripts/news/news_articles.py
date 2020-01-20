import pandas as pd
import json
import spacy
import sys
import os
import operator
import re
import numpy as np

df = pd.read_csv('./data/news/combined_news_csv.csv')

def get_sentiment(sentiment_string):
    if(sentiment_string == 'Negative'):
        return -1
    elif sentiment_string == 'Positive':
        return 1
    else:
        return 0

df['sentiment'] = df['Final_Sentiment'].apply(get_sentiment)

# df_lib = df[df['lib'] == 1]
# df_cpc = df[df['cpc'] == 1]
# df_ndp = df[df['ndp'] == 1]

# print(df.head())

sp = spacy.load('en_core_web_sm') 
# df = pd.DataFrame(columns=['Headline','Description','Summary','URL','sentiment','Final_Sentiment','Final_Sentiment_Probability', 'lib', 'cpc', 'ndp'])
# df = pd.read_csv('./Data/News/party-tags.csv', index_col=None, header=0)
parties_tag_df = df[['Headline','Description','Summary','URL','sentiment','Final_Sentiment','Final_Sentiment_Probability', 'lib', 'cpc', 'ndp']]

# parties_tag_df = parties_tag[['Headline','Description','Summary','URL','sentiment','Final_Sentiment','Final_Sentiment_Probability', 'lib', 'cpc', 'ndp']]
parties_tag_df = parties_tag_df[parties_tag_df['Summary'].notnull()]
positives = parties_tag_df[parties_tag_df.Final_Sentiment.isin(['Positive'])]
negatives = parties_tag_df[parties_tag_df.Final_Sentiment.isin(['Negative'])]
neurals = parties_tag_df[parties_tag_df.Final_Sentiment.isin(['Neutral'])]

def getPartyTags(party, count):
    if party is not 'all':
        pos = positives[positives[party].isin([1])].nlargest(count, 'Final_Sentiment_Probability')
        neg = negatives[negatives[party].isin([1])].nlargest(count, 'Final_Sentiment_Probability')
        neu = neurals[neurals[party].isin([1])].nlargest(count, 'Final_Sentiment_Probability')
    else:
        pos = positives.nlargest(count, 'Final_Sentiment_Probability')
        neg = negatives.nlargest(count, 'Final_Sentiment_Probability')
        neu = neurals.nlargest(count, 'Final_Sentiment_Probability')

    tags = pd.concat([pos, neg, neu],ignore_index=False).sort_values(by=['Final_Sentiment_Probability'], ascending=False)
    tags = tags[['Headline','Description','Summary','URL','sentiment']]
    return tags

all_tags = getPartyTags('all', 5).to_dict('records')
cpc_tags = getPartyTags('cpc', 5).to_dict('records')
lib_tags = getPartyTags('lib', 5).to_dict('records')
ndp_tags = getPartyTags('ndp', 5).to_dict('records')

final_tags = {}

final_tags['all'] = all_tags
final_tags['CPC'] = cpc_tags
final_tags['LPC'] = lib_tags
final_tags['NDP'] = ndp_tags

with open('./dashboard/public/static/newsArticles.json', 'w') as file:
    json.dump(final_tags, file, indent=4, separators=(',', ': '))

# with open('./dashboard/public/static/candidateNews.json', 'w') as file:
#     json.dump(dictionary, file)

