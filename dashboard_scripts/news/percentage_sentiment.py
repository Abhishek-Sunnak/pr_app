import json
import pandas as pd

def get_percentage_sentiment(d, key_start, dictionary):
    negative = len(d[d['sentiment'] < 0])
    positive = len(d[d['sentiment'] > 0])
    neutral = len(d[d['sentiment'] == 0])
    total_length = negative + positive + neutral
    
    positive_percentage = round(positive * 100 / total_length)
    negative_percentage = round(negative * 100 / total_length)
    neutral_percentage = 100 - positive_percentage - negative_percentage

    dictionary[key_start + 'Positive'] = positive_percentage
    dictionary[key_start + 'Negative'] = negative_percentage
    dictionary[key_start + 'Neutral'] = neutral_percentage
    
    return dictionary

def get_percentage_sentiment_for_all(df):
  df_lib = df[df['lib'] == 1]
  df_cpc = df[df['cpc'] == 1]
  df_ndp = df[df['ndp'] == 1]
  dictionary = {}
  dictionary = get_percentage_sentiment(df_lib, 'lpc', dictionary)
  dictionary = get_percentage_sentiment(df_cpc, 'cpc', dictionary)
  dictionary = get_percentage_sentiment(df_ndp, 'ndp', dictionary)

  with open('./dashboard/public/static/candidateNews.json', 'w') as file:
    json.dump(dictionary, file)

df = pd.read_csv('./data/news/combined_news_csv.csv')

def get_sentiment(sentiment_string):
    if(sentiment_string == 'Negative'):
        return -1
    elif sentiment_string == 'Positive':
        return 1
    else:
        return 0

df['sentiment'] = df['Final_Sentiment'].apply(get_sentiment)

get_percentage_sentiment_for_all(df)