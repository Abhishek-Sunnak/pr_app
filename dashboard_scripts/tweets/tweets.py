import pandas as pd
import json

df = pd.read_csv('./data/twitter/cleaned.csv')
unique_tweets = df.drop_duplicates(subset=['Text_clean'])
print(unique_tweets.columns)
def get_sentiment(sentiment):
    if(sentiment == 'Positive'):
        return 1
    elif sentiment == 'Neutral':
        return 0
    else:
        return -1
unique_tweets['sentiment'] = unique_tweets['Final_Sentiment'].apply(get_sentiment)
positives = unique_tweets[unique_tweets.Final_Sentiment.isin(['Positive'])]
negatives = unique_tweets[unique_tweets.Final_Sentiment.isin(['Negative'])]
neurals = unique_tweets[unique_tweets.Final_Sentiment.isin(['Neutral'])]

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
    tags['id'] = tags['id'].astype(str)
    tags['sentiment'] = tags['sentiment'].astype(int)
    tags = tags[['id','sentiment']]
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

with open('./dashboard/public/static/tweets.json', 'w') as file:
    json.dump(final_tags, file, indent=4, separators=(',', ': '))
