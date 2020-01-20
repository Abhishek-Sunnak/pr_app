import pandas as pd
import json

df = pd.read_csv('./data/news/combined_news_csv.csv')

def get_sentiment(sentiment_string):
    if(sentiment_string == 'Negative'):
        return -1
    elif sentiment_string == 'Positive':
        return 1
    else:
        return 0

df['sentiment'] = df['Final_Sentiment'].apply(get_sentiment)

left = df[df['Bias'] == '__label__left']
left_centric = df[df['Bias'] == '__label__left-center']
right = df[df['Bias'] == '__label__right']
right_centric = df[df['Bias'] == '__label__right-center']
centric = df[df['Bias'] == '__label__least']

def getBiasStackedData(d):
    item = {}
    lib_d = d[d['lib'] == 1]
    cpc_d = d[d['cpc'] == 1]
    ndp_d = d[d['ndp'] == 1]
    item['CPC'] = getSentiment(cpc_d)
    item['LPC'] = getSentiment(lib_d)
    item['NDP'] = getSentiment(ndp_d)
    return item
    
def getSentiment(d):
    negative = len(d[d['sentiment'] < 0])
    positive = len(d[d['sentiment'] > 0])
    neutral = len(d[d['sentiment'] == 0])
    total_length = negative + positive + neutral
    
    if(total_length == 0):
        positive_percentage = 0
        negative_percentage = 0
        neutral_percentage = 0
    else:
        positive_percentage = round(positive * 100 / total_length)
        negative_percentage = round(negative * 100 / total_length)
        neutral_percentage = 100 - positive_percentage - negative_percentage
    
    return {
        'positive': positive_percentage,
        'negative': negative_percentage,
        'neutral': neutral_percentage
    }

dictionary = {
    'all': getBiasStackedData(df),
    'Left': getBiasStackedData(left),
    'Right': getBiasStackedData(right),
    'Left Centric': getBiasStackedData(left_centric),
    'Right Centric': getBiasStackedData(right_centric),
    'No Bias': getBiasStackedData(centric),
}

with open('./dashboard/public/static/biasStackedBarChart.json', 'w') as file:
    json.dump(dictionary, file)