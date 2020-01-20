import glob
import pandas as pd
from bs4 import BeautifulSoup
import re
import itertools
import emoji
import numpy as np
import fastText
import spacy
from spacy import displacy
import ast
import math
import sys

from  geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
geolocator=Nominatim(timeout=50, user_agent="my-application")

def load_dict_contractions():
  return {
    "ain't":"is not","amn't":"am not","aren't":"are not","can't":"cannot","'cause":"because",
    "couldn't":"could not","couldn't've":"could not have","could've":"could have","daren't":"dare not",
    "daresn't":"dare not","dasn't":"dare not","didn't":"did not","doesn't":"does not","don't":"do not",
    "e'er":"ever","em":"them","everyone's":"everyone is","finna":"fixing to","gimme":"give me",
    "gonna":"going to","gon't":"go not","gotta":"got to","hadn't":"had not","hasn't":"has not",
    "haven't":"have not","he'd":"he would","he'll":"he will","he's":"he is","he've":"he have",
    "how'd":"how would","how'll":"how will","how're":"how are","how's":"how is","i'd":"i would","I'd":"I would",
    "I'll":"I will","i'm":"i am","I'm":"I am","I'm'a":"I am about to","I'm'o":"I am going to","isn't":"is not",
    "it'd":"it would","it'll":"it will","it's":"it is","I've":"I have","kinda":"kind of","let's":"let us",
    "mayn't":"may not","may've":"may have","mightn't":"might not","might've":"might have","mustn't":"must not",
    "mustn't've":"must not have","must've":"must have","needn't":"need not","ne'er":"never","o'":"of",
    "o'er":"over","ol'":"old","oughtn't":"ought not","shalln't":"shall not","shan't":"shall not","she'd":"she would",
    "she'll":"she will","she's":"she is","shouldn't":"should not","shouldn't've":"should not have",
    "should've":"should have","somebody's":"somebody is","someone's":"someone is","something's":"something is",
    "that'd":"that would","that'll":"that will","that're":"that are","that's":"that is","there'd":"there would",
    "there'll":"there will","there're":"there are","there's":"there is","these're":"these are","they'd":"they would",
    "they'll":"they will","they're":"they are","they've":"they have","this's":"this is","those're":"those are","'tis":"it is",
    "'twas":"it was","wanna":"want to","wasn't":"was not","we'd":"we would","we'd've":"we would have","we'll":"we will",
    "we're":"we are","weren't":"were not","we've":"we have","what'd":"what did","what'll":"what will","what're":"what are",
    "what's":"what is","what've":"what have","when's":"when is","where'd":"where did","where're":"where are","where's":"where is",
    "where've":"where have","which's":"which is","who'd":"who would","who'd've":"who would have","who'll":"who will",
    "who're":"who are","who's":"who is","who've":"who have","why'd":"why did","why're":"why are","why's":"why is",
    "won't":"will not","wouldn't":"would not","would've":"would have","y'all":"you all","you'd":"you would",
    "you'll":"you will","you're":"you are","you've":"you have","Whatcha":"What are you","luv":"love","sux":"sucks"
  }

def load_dict_smileys():
  return {
    ":‑)":"smiley",":-]":"smiley",":-3":"smiley",":->":"smiley","8-)":"smiley",":-}":"smiley",":)":"smiley",
    ":]":"smiley",":3":"smiley",":>":"smiley","8)":"smiley",":}":"smiley",":o)":"smiley",":c)":"smiley",
    ":^)":"smiley","=]":"smiley","=)":"smiley",":-))":"smiley",":‑D":"smiley","8‑D":"smiley","x‑D":"smiley",
    "X‑D":"smiley",":D":"smiley","8D":"smiley","xD":"smiley","XD":"smiley",":‑(":"sad",":‑c":"sad",":‑<":"sad",
    ":‑[":"sad",":(":"sad",":c":"sad",":<":"sad",":[":"sad",":-||":"sad",">:[":"sad",":{":"sad",":@":"sad",
    ">:(":"sad",":'‑(":"sad",":'(":"sad",":‑P":"playful","X‑P":"playful","x‑p":"playful",":‑p":"playful",
    ":‑Þ":"playful",":‑þ":"playful",":‑b":"playful",":P":"playful","XP":"playful","xp":"playful",":p":"playful",
    ":Þ":"playful",":þ":"playful",":b":"playful","<3":"love"
  }

def tweet_cleaning_for_sentiment_analysis(tweet):    
    
    #Escaping HTML characters
    tweet = BeautifulSoup(tweet, 'html.parser').get_text()

    #Special case not handled previously.
    tweet = tweet.replace('\x92',"'")
    tweet = tweet.replace('"',"'")
    tweet = tweet.replace("…",".")
    tweet = tweet.replace("\\\'","'")
    tweet = tweet.replace("#","")
    tweet = tweet.replace("—","")
    
    #Removal of hastags/account
    tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", tweet).split())
    
    #Removal of address
    tweet = ' '.join(re.sub("(\w+:\/\/\S+)", " ", tweet).split())
    
    #Removal of Punctuation
    tweet = ' '.join(re.sub("[\[\]\'\\\.\,\!\?\:\;\-\=]", " ", tweet).split())
    
    #Lower case
    tweet = tweet.lower()
    
    #CONTRACTIONS source: https://en.wikipedia.org/wiki/Contraction_%28grammar%29
    CONTRACTIONS = load_dict_contractions()
    tweet = tweet.replace("’","'")
    tweet = tweet.replace("   "," ")
    tweet = tweet.replace("  "," ")
    words = tweet.split()
    reformed = [CONTRACTIONS[word] if word in CONTRACTIONS else word for word in words]
    tweet = " ".join(reformed)
    
    # Standardizing words
    tweet = ''.join(''.join(s)[:2] for _, s in itertools.groupby(tweet))
    
    #Deal with emoticons source: https://en.wikipedia.org/wiki/List_of_emoticons
    SMILEY = load_dict_smileys()  
    words = tweet.split()
    reformed = [SMILEY[word] if word in SMILEY else word for word in words]
    tweet = " ".join(reformed)
    
    #Deal with emojis
    tweet = emoji.demojize(tweet)

    tweet = tweet.replace(":"," ")
    tweet = ' '.join(tweet.split())

    return tweet

def get_sentiment(text):
  if text==text:
    sent = model.predict([text],k=1)[0][0][0]
  else:
    sent = np.nan
  return sent

def get_prob(text):
    if text==text:
        sent = model.predict([text],k=1)[1][0][0]
    else:
        sent = 0
    return sent

atlantic = ['Nova Scotia', 'Prince Edward Island', 'New Brunswick', 'Newfoundland and Labrador']
praires = ['Saskatchewan', 'Manitoba']

def getRegion(province):
    if province in atlantic:
        return 'Atlantic'
    elif province in praires:
        return 'Praires'
    elif province == "Québec":
        return 'Quebec'
    else:
        return province

def getProvince(user):
  try:
    user = ast.literal_eval(user)
    location = user['location']
    if len(location):
      loc = geolocator.geocode(location, addressdetails=True)
      if loc is not None:
        address = loc.raw['address']
        if 'country' in address and address['country'] == 'Canada':
          if 'state' in address:
            return address['state']
          else:
            return 'N/A'
        else:
          return 'N/A'
      else:
        return 'N/A'
    else:
        return 'N/A'
  except:
    print(sys.exc_info()[0])
    return 'N/A'
nlp = spacy.load("en_core_web_sm")
def get_noun_phrases(text):
  noun_chunk = list()
  for i in nlp(text).noun_chunks:
    noun_chunk.append(str(i))
  return " ".join(noun_chunk)

all_file_names = glob.glob(r'./data/twitter/twitter_canada' + "*.csv")
all_files = []

for filename in all_file_names:
    df = pd.read_csv(filename, index_col=None, header=0)
    all_files.append(df)

twitter_data = pd.concat(all_files, axis=0, ignore_index=True)
twitter_data = twitter_data.drop_duplicates(["created_at","id"]).reset_index()
twitter_data["Text_clean"] = twitter_data["full_text"].apply(tweet_cleaning_for_sentiment_analysis)

model = fastText.load_model("./data/models/model-en3.ftz")
twitter_data["sentiment8"] = twitter_data["Text_clean"].apply(get_sentiment)
twitter_data["sentiment_prob8"] = twitter_data["Text_clean"].apply(get_prob)

model = fastText.load_model("./data/models/model-en5.ftz")
twitter_data["sentiment5"] = twitter_data["Text_clean"].apply(get_sentiment)
twitter_data["sentiment_prob5"] = twitter_data["Text_clean"].apply(get_prob)

model = fastText.load_model("./data/models/model-en_org2.ftz")
twitter_data["sentiment2"] = twitter_data["Text_clean"].apply(get_sentiment)
twitter_data["sentiment_prob2"] = twitter_data["Text_clean"].apply(get_prob)

twitter_data["Negative"] = (twitter_data[["sentiment5","sentiment8","sentiment2"]] == "__label__NEGATIVE").sum(1)
twitter_data["Positive"] = (twitter_data[["sentiment5","sentiment8","sentiment2"]] == "__label__POSITIVE").sum(1)
twitter_data["Neutral"] = (twitter_data[["sentiment5","sentiment8","sentiment2"]] == "__label__NEUTRAL").sum(1)

twitter_data["Final_Sentiment"] = twitter_data[["Neutral","Positive","Negative"]].idxmax(axis=1)
twitter_data["Final_Sentiment_Probability"] = twitter_data[["sentiment_prob8","sentiment_prob5", "sentiment_prob2"]].max(axis=1)
twitter_data["Noun_phrases"] = twitter_data["Text_clean"].apply(get_noun_phrases)

length = len(twitter_data)
itemrange = 1000
iternum = math.ceil(length / itemrange)
start = 0
end = start + itemrange
province_series = pd.Series()
print(iternum)
for i in range(iternum):
  tw = twitter_data[start:end]
  print(start, end)
  tw_ps = tw["user"].apply(getProvince)
  province_series = province_series.append(tw_ps, ignore_index=False)
  start = end
  if(end + itemrange > (length - 1) ):
    end = length
  else:
    end += itemrange
  print(tw_ps)

twitter_data["province"] = province_series
twitter_data["region"] = twitter_data["province"].apply(getRegion)

partiesObj = {
    'lib': ['liberal', 'liberals', 'lpc', 'lib', 'left'],
    'cpc': ['conservative', 'conservatives', 'cpc', 'con', 'right'],
    'ndp': ['ndp', 'democratic', 'democrat', 'democrats']
}

def tagTweet(tweet):
    tweetCopy = tweet
    partyList = {
        'lib': 0,
        'cpc': 0,
        'ndp': 0
    }

    justinCount = 0
    scheerCount = 0
    lavalinCount = 0
    singhCount = 0

    if "justin trudeau" in tweetCopy and justinCount == 0:
        justinCount += 1
        partyList['lib'] += 1
        tweetCopy = tweetCopy.replace('justin trudeau','')
    if "justin" in tweetCopy and justinCount == 0:
        justinCount += 1
        partyList['lib'] += 1
        tweetCopy = tweetCopy.replace('justin','')
    if "trudeau" in tweetCopy and justinCount == 0:
        justinCount += 1
        partyList['lib'] += 1
        tweetCopy = tweetCopy.replace('trudeau','')

    if "andrew scheer" in tweetCopy and scheerCount == 0:
        scheerCount += 1
        partyList['cpc'] += 1
        tweetCopy = tweetCopy.replace('andrew scheer','')
    if "andrew" in tweetCopy and scheerCount == 0:
        scheerCount += 1
        partyList['cpc'] += 1
        tweetCopy = tweetCopy.replace('andrew','')
    if "scheer" in tweetCopy and scheerCount == 0:
        scheerCount += 1
        partyList['cpc'] += 1
        tweetCopy = tweetCopy.replace('scheer','')

    if "snc-lavalin" in tweetCopy and lavalinCount == 0:
        lavalinCount += 1
        partyList['lib'] += 1
        tweetCopy = tweetCopy.replace('snc-lavalin','')
    if "snc" in tweetCopy and lavalinCount == 0:
        lavalinCount += 1
        partyList['lib'] += 1
        tweetCopy = tweetCopy.replace('snc','')
    if "lavalin" in tweetCopy and lavalinCount == 0:
        lavalinCount += 1
        partyList['lib'] += 1
        tweetCopy = tweetCopy.replace('lavalin','')

    if "jagmeet singh" in tweetCopy and singhCount == 0:
        singhCount += 1
        partyList['ndp'] += 1
        tweetCopy = tweetCopy.replace('jagmeet singh','')
    if "jagmeet" in tweetCopy and singhCount == 0:
        singhCount += 1
        partyList['ndp'] += 1
        tweetCopy = tweetCopy.replace('jagmeet','')
    if "singh" in tweetCopy and singhCount == 0:
        singhCount += 1
        partyList['ndp'] += 1
        tweetCopy = tweetCopy.replace('singh','')
    
    tweets = nlp(tweetCopy)
    tokens = [i.text.strip() for i in tweets]
    for token in tokens:
        if token in partiesObj['lib']:
            partyList['lib'] += 1  
        if token in partiesObj['cpc']:
            partyList['cpc'] += 1
        if token in partiesObj['ndp']:
            partyList['ndp'] += 1

    return partyList

lib = []
cpc = []
ndp = []
parties = []

for tweet in twitter_data.Text_clean:
    tweet = re.sub(r'\brt\b', '', tweet)  # Remove RT (retweet)
    tag = tagTweet(tweet)
    maxi = max(tag, key=tag.get)
    maxCount = tag[maxi]
    keys = tag.keys()
    highestTag = [k for k in keys if tag[k] == maxCount]
    emptyTags = (list(set(keys) - set(highestTag)))

    if len(emptyTags) is 0 and len(highestTag) is 3:
        lib.append(0)
        cpc.append(0)
        ndp.append(0)
    else:
        for i in highestTag:
            if i == 'lib':
                tag['lib'] = 1
            if i == 'cpc':
                tag['cpc'] = 1
            if i == 'ndp':
                tag['ndp'] = 1
        
        for i in emptyTags:
            if i == 'lib':
                tag['lib'] = 0
            if i == 'cpc':
                tag['cpc'] = 0
            if i == 'ndp':
                tag['ndp'] = 0

        lib.append(tag['lib'])
        cpc.append(tag['cpc'])
        ndp.append(tag['ndp'])

twitter_data['lib'] = lib
twitter_data['cpc'] = cpc
twitter_data['ndp'] = ndp

lib = (twitter_data['lib'] == 1)
cpc = (twitter_data['cpc'] == 1)
ndp = (twitter_data['ndp'] == 1)
twitter_data = twitter_data[lib | cpc | ndp]

twitter_data.to_csv('./data/twitter/cleaned.csv')