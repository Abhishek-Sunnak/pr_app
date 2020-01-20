import pandas as pd
import sys
import os
import re
import string
from collections import Counter
import spacy
import json
import emoji
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']

more_stop_words = ['canada', "jagmeetsingh", "canadians", 'rt', "justin", 'jagmeet', 'trudeau', "scheer", "singh", "andrew", "canadian", "party", "ndp", "lpc", 
                    "lib", "cpc", "liberals", "liberal", "pm", "conservatives", "conservative", "con", "democrats", "democratic"]
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def getTokens(article):
    article = str(article)
    tokenized_article = tokens_re.findall(article)
    tokenized_article = [token if emoticon_re.search(token) else token.lower() for token in tokenized_article]
    return [word for word in tokenized_article if word not in stop and len(word) > 1 and word not in more_stop_words] 
df = pd.DataFrame(columns=['Headline','Description', 'Bias', 'Full_text', 'Noun_phrases', 'sentiment', 'Final_Sentiment', 'lib', 'cpc', 'ndp', 'parties'])
df = pd.read_csv('./data/news/combined_news_csv.csv')

def get_sentiment(sentiment_string):
    if(sentiment_string == 'Negative'):
        return -1
    elif sentiment_string == 'Positive':
        return 1
    else:
        return 0

df['sentiment'] = df['Final_Sentiment'].apply(get_sentiment)

# df = pd.read_csv('./data/news/party-tags.csv', index_col=None, header=0)
df = df[['Headline','Description', 'Bias', 'Full_text', 'sentiment', 'Final_Sentiment', 'lib', 'cpc', 'ndp', 'Noun_phrases']]

df_lib = df[df['lib'].isin([1])]
df_cpc = df[df['cpc'].isin([1])]
df_ndp = df[df['ndp'].isin([1])]
    
def getTopWords(data, count):
    count_all_words = Counter()
    for article in data.Noun_phrases:
        tokens  = getTokens(article)
        words = tokens
        count_all_words.update(words)
    words_freq = count_all_words.most_common(count)
    return words_freq

all_word_frequency = getTopWords(df, 50)
lpc_word_frequency = getTopWords(df_lib, 50)
cpc_word_frequency  = getTopWords(df_cpc, 50)
ndp_word_frequency = getTopWords(df_ndp, 50)

def get_count(data):
    wordcloud = []
    for i in data:
        freq = {}
        freq['text'] = i[0]
        freq['value'] = i[1]
        wordcloud.append(freq)
        analysis = TextBlob(i[0])
        polarity = analysis.sentiment.polarity
        if polarity > 0:
            freq['sentiment'] = 1
        elif polarity == 0:
            freq['sentiment'] = 0
        else:
            freq['sentiment'] = -1
    return wordcloud

words = {}
words['LPC'] = get_count(lpc_word_frequency)
words['CPC'] = get_count(cpc_word_frequency)
words['NDP'] = get_count(ndp_word_frequency)
words['all'] = get_count(all_word_frequency)

with open('./dashboard/public/static/newsWordCloud.json', 'w') as file:
    json.dump(words, file, indent=4, separators=(',', ': '))