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
 
def getTokens(tweet, option):
    tweet = str(tweet)
    tweet = re.sub('\d+', ' ',tweet) # Remove numbers in tweets
    tweet = re.sub(r'@[A-Za-z0-9]+', '', tweet) # Remove usernames mention from tweets
    tweet = re.sub(r'\brt\b', '', tweet)  # Remove RT (retweet)
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet) # Remove urls in tweets
    tweet = emoji.demojize(tweet) #remove smileys
    
    tokenized_tweet = tokens_re.findall(tweet)
    tokenized_tweet = [token if emoticon_re.search(token) else token.lower() for token in tokenized_tweet]
    if option is 'word':
        return [word for word in tokenized_tweet if word not in stop and len(word) > 1 and word not in more_stop_words] 
    if option is 'hashtags':
        return [word for word in tokenized_tweet if word.startswith('#') and len(word) > 1]

df = pd.DataFrame(columns=['id', 'full_text', 'Text_clean', 'Noun_phrases', 'sentiment', 'Final_Sentiment', 'lib', 'cpc', 'ndp', 'parties'])
df = pd.read_csv('./data/twitter/cleaned.csv')
df = df[['id', 'full_text', 'Text_clean', 'Noun_phrases', 'Final_Sentiment', 'lib', 'cpc', 'ndp']]

df_lib = df[df['lib'].isin([1])]
df_cpc = df[df['cpc'].isin([1])]
df_ndp = df[df['ndp'].isin([1])]
    
def getTopWords(data, count):
    count_all_words = Counter()
    for tweet in data.Noun_phrases:
        tokens  = getTokens(tweet, 'word')
        words = tokens
        count_all_words.update(words)
    words_freq = count_all_words.most_common(count)
    return words_freq

def getTopHashtags(data, count):
    count_all_hashtags = Counter()
    for tweet in data.full_text:
        tokens  = getTokens(tweet, 'hashtags')
        hashtags = tokens
        count_all_hashtags.update(hashtags)
    hashtags_freq = count_all_hashtags.most_common(count)
    return hashtags_freq

all_word_frequency = getTopWords(df, 30)
lpc_word_frequency = getTopWords(df_lib, 30)
cpc_word_frequency  = getTopWords(df_cpc, 30)
ndp_word_frequency = getTopWords(df_ndp, 30)

all_hashtag_frequency = getTopHashtags(df, 30)
lpc_hashtag_frequency = getTopHashtags(df_lib, 30)
cpc_hashtag_frequency = getTopHashtags(df_cpc, 30)
ndp_hashtag_frequency = getTopHashtags(df_ndp, 30)

def get_count(data):
    lib_hashtags = []
    for i in data:
        freq = {}
        freq['text'] = i[0]
        freq['value'] = i[1]
        lib_hashtags.append(freq)
        analysis = TextBlob(i[0])
        polarity = analysis.sentiment.polarity
        if polarity > 0:
            freq['sentiment'] = 1
        elif polarity == 0:
            freq['sentiment'] = 0
        else:
            freq['sentiment'] = -1
    return lib_hashtags
hashtags = {}
hashtags['LPC'] = get_count(lpc_hashtag_frequency)
hashtags['CPC'] = get_count(cpc_hashtag_frequency)
hashtags['NDP'] = get_count(ndp_hashtag_frequency)
hashtags['all'] = get_count(all_hashtag_frequency)

words = {}
words['LPC'] = get_count(lpc_word_frequency)
words['CPC'] = get_count(cpc_word_frequency)
words['NDP'] = get_count(ndp_word_frequency)
words['all'] = get_count(all_word_frequency)

with open('./dashboard/public/static/wordCloudHashtagsData.json', 'w') as file:
    json.dump(hashtags, file, indent=4, separators=(',', ': '))

with open('./dashboard/public/static/wordCloudData.json', 'w') as file:
    json.dump(words, file, indent=4, separators=(',', ': '))