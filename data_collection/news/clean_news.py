import glob
import pandas as pd
import nltk
import spacy
nltk.download('gutenberg')
from nltk.corpus import gutenberg
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
import heapq
import re
from nltk.corpus import stopwords
import fastText
import itertools
import numpy as np
from bs4 import BeautifulSoup
import emoji

all_files = glob.glob(r'./data/News/Can' + "*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

news_data = pd.concat(li, axis=0, ignore_index=True)
# news_data

combined_df_dedup=news_data.drop_duplicates(subset=['Headline','URL'], keep="first")

combined_df_dedup.index=range(len(combined_df_dedup))

search_words = pd.read_excel('./data/Keywords/News.xlsx', 'Filtering_search_words')['keywords'].tolist()
search_words = [word.lower() for word in search_words]
def search_queries(description):
    for word in search_words:
        if type(description) != str:
            print(description)
        if description.lower().find(word) != -1:
            return True
    return False
temp_df = combined_df_dedup['Full_text'].fillna('')
filter_flags = temp_df.apply(search_queries)

combined_df_dedup = combined_df_dedup[filter_flags == True]

text = ""
for file_id in gutenberg.fileids():
    text += gutenberg.raw(file_id)

trainer = PunktTrainer()
trainer.INCLUDE_ALL_COLLOCS = True
trainer.train(text)

def get_relevant_sent(text):
    sentences_org=tokenizer.tokenize(text)
    text = text.lower()
    sentences=tokenizer.tokenize(text)
    indexes = list()
    for key in senetence_relevance_words:
        matching = [s for s in sentences if key in s]
        for text in matching:
            indexes.append(sentences.index(text))
    next_index = [x+1 for x in indexes]
    prev_index = [x-1 for x in indexes]
    comb_indexes = indexes + next_index + prev_index
    final_indexes = list(filter(lambda x: (x <= len(sentences)-1) & (x >= 0), comb_indexes))
    final_indexes.sort()
    final_indexes = list(set(final_indexes))
    rel_sent_list=list()
    for index in final_indexes:
        rel_sent_list.append(sentences_org[index])

    return ' '.join(rel_sent_list)

tokenizer = PunktSentenceTokenizer(trainer.get_params())
extra_abbreviations = ['dr', 'vs', 'mr', 'mrs', 'prof', 'inc', 'i.e',"jan","feb","mar","apr","may","jun","jul"
                       ,"aug","sep","oct","nov","dec","b.c","e.g","a.m","p.m","c.d","u.s","can","u.k","u.n"
                      ]
tokenizer._params.abbrev_types.update(extra_abbreviations)

senetence_relevance_words = pd.read_excel('./data/Keywords/News.xlsx', 'Senetence_Relevance_Words')['keywords'].tolist()
combined_df_dedup = combined_df_dedup[combined_df_dedup.Full_text != "Empty"]
combined_df_dedup = combined_df_dedup[combined_df_dedup["Full_text"].notna()]

combined_df_dedup["rel_sent"] = combined_df_dedup["Full_text"].apply(get_relevant_sent)

combined_df_dedup = combined_df_dedup[["Category","Date_published","Description","Full_text","Headline","Provider","URL","rel_sent"]]

combined_df_dedup['key'] = range(1, len(combined_df_dedup.index)+1)

nlp = spacy.load('en_core_web_sm')
def normalize_text(text):
  text = str(text)
  tm1 = re.sub('<pre>.*?</pre>', '', text, flags=re.DOTALL)
  tm2 = re.sub('<code>.*?</code>', '', tm1, flags=re.DOTALL)
  tm3 = re.sub('<[^>]+>©', '', tm1, flags=re.DOTALL)
  return tm3.replace("\n", "")
news_text = combined_df_dedup[['Full_text','key']]
news_text = news_text[news_text.Full_text != "Empty"]

news_text['Full_text_1'] = news_text['Full_text'].apply(normalize_text)


punctuations = '!"#$%&\'()*+,-/:;<=>?@[\\]^_`{|}~©'
stopwords = stopwords.words('english')
def cleanup_text(docs, logging=False):
    texts = []
    doc = nlp(docs, disable=['parser', 'ner'])
    tokens = [tok.lemma_.lower().strip() for tok in doc if tok.lemma_ != '-PRON-']
    tokens = [tok for tok in tokens if tok not in stopwords and tok not in punctuations]
    tokens = ' '.join(tokens)
    texts.append(tokens)
    return pd.Series(texts)
news_text['Full_text'] = news_text['Full_text_1'].apply(lambda x: cleanup_text(x, False))

def generate_summary(text_without_removing_dot, cleaned_text):
  sample_text = text_without_removing_dot
  doc = nlp(sample_text)
  sentence_list=[]
  for idx, sentence in enumerate(doc.sents): # we are using spacy for sentence tokenization
    sentence_list.append(re.sub(r'[^\w\s]','',str(sentence)))

  stopwords = nltk.corpus.stopwords.words('english')

  word_frequencies = {}  
  for word in nltk.word_tokenize(cleaned_text):  
    if word not in stopwords:
      if word not in word_frequencies.keys():
        word_frequencies[word] = 1
      else:
        word_frequencies[word] += 1


  maximum_frequncy = max(word_frequencies.values())

  for word in word_frequencies.keys():  
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)


  sentence_scores = {}  
  for sent in sentence_list:  
    for word in nltk.word_tokenize(sent.lower()):
      if word in word_frequencies.keys():
        if len(sent.split(' ')) < 30:
          if sent not in sentence_scores.keys():
            sentence_scores[sent] = word_frequencies[word]
          else:
            sentence_scores[sent] += word_frequencies[word]


  summary_sentences = heapq.nlargest(10, sentence_scores, key=sentence_scores.get)

  summary = " ".join(summary_sentences)
  return summary

news_text["Summary"]="Empty"
news_text.index=range(len(news_text))
for row in range(len(news_text)):
    news_text.iloc[row, news_text.columns.get_loc('Summary')] = generate_summary(news_text['Full_text_1'][row], news_text['Full_text'][row])

news2=pd.merge(combined_df_dedup[["Category","Date_published","Description","Full_text","Headline","Provider","URL","rel_sent","key"]],news_text[["Summary","key"]], on='key', how='left')

# emoticons
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

# self defined contractions
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


def tweet_cleaning_for_sentiment_analysis(tweet):    
  #Escaping HTML characters
  tweet = BeautifulSoup(tweet).get_text()

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
      text_clean = tweet_cleaning_for_sentiment_analysis(text)
      sent = model.predict([text_clean],k=1)[0][0][0]
  else:
      sent = np.nan
  return sent

def get_prob(text):
  if text==text:
      text_clean = tweet_cleaning_for_sentiment_analysis(text)
      sent = model.predict([text_clean],k=1)[1][0][0]
  else:
      sent = 0
  return sent

news2 = news2[news2.Headline != "Empty"]
news2 = news2[news2["Headline"].notna()]
model = fastText.load_model("./data/Models/model_bias.ftz")

news2["Bias"] = news2["Full_text"].apply(get_sentiment)
news2["Bias_prob"] = news2["Full_text"].apply(get_prob)

model = fastText.load_model("./data/Models/amazon_review_full.bin")

news2["sentiment_amz_full"] = news2["Full_text"].apply(get_sentiment)
news2["sentiment_amz_full_prob"] = news2["Full_text"].apply(get_prob)

news2["sentiment_amz_rel"] = news2["rel_sent"].apply(get_sentiment)
news2["sentiment_amz_rel_prob"] = news2["rel_sent"].apply(get_prob)

news2.loc[news2.sentiment_amz_full == "__label__1", 'Final_Sentiment'] = 'Negative'
news2.loc[news2.sentiment_amz_full == "__label__2", 'Final_Sentiment'] = 'Neutral'
news2.loc[news2.sentiment_amz_full == "__label__3", 'Final_Sentiment'] = 'Neutral'
news2.loc[news2.sentiment_amz_full == "__label__4", 'Final_Sentiment'] = 'Neutral'
news2.loc[news2.sentiment_amz_full == "__label__5", 'Final_Sentiment'] = 'Positive'


news2.loc[news2.sentiment_amz_rel == "__label__1", 'Final_Sentiment'] = 'Negative'
news2.loc[news2.sentiment_amz_rel == "__label__2", 'Final_Sentiment'] = 'Neutral'
news2.loc[news2.sentiment_amz_rel == "__label__3", 'Final_Sentiment'] = 'Neutral'
news2.loc[news2.sentiment_amz_rel == "__label__4", 'Final_Sentiment'] = 'Neutral'
news2.loc[news2.sentiment_amz_rel == "__label__5", 'Final_Sentiment'] = 'Positive'

news2["Final_Sentiment_Probability"] = news2[["sentiment_amz_full_prob","sentiment_amz_rel_prob"]].max(axis=1)

def get_noun_phrases(text):
    noun_chunk = list()
    for i in nlp(text).noun_chunks:
        noun_chunk.append(str(i))
    return " ".join(noun_chunk)

news2["Noun_phrases"] = news2["Full_text"].apply(get_noun_phrases)

partiesObj = {
    'lib': ['liberal', 'liberals', 'lpc', 'lib', 'left'],
    'cpc': ['conservative', 'conservatives', 'cpc', 'con', 'right'],
    'ndp': ['ndp', 'democratic', 'democrat', 'democrats']
}

def tagNews(article):
    articleCopy = article
    partyList = {
        'lib': 0,
        'cpc': 0,
        'ndp': 0
    }

    justinCount = 0
    scheerCount = 0
    singhCount = 0
    lavalinCount = 0

    if "justin trudeau" in articleCopy and justinCount == 0:
        justinCount += 1
        partyList['lib'] += 1
        articleCopy = articleCopy.replace('justin trudeau','')
    if "justin" in articleCopy and justinCount == 0:
        justinCount += 1
        partyList['lib'] += 1
        articleCopy = articleCopy.replace('justin','')
    if "trudeau" in articleCopy and justinCount == 0:
        justinCount += 1
        partyList['lib'] += 1
        articleCopy = articleCopy.replace('trudeau','')

    if "snc-lavalin" in articleCopy and lavalinCount == 0:
        lavalinCount += 1
        partyList['lib'] += 1
        articleCopy = articleCopy.replace('snc-lavalin','')
    if "snc" in articleCopy and lavalinCount == 0:
        lavalinCount += 1
        partyList['lib'] += 1
        articleCopy = articleCopy.replace('snc','')
    if "lavalin" in articleCopy and lavalinCount == 0:
        lavalinCount += 1
        partyList['lib'] += 1
        articleCopy = articleCopy.replace('lavalin','')

    if "andrew scheer" in articleCopy and scheerCount == 0:
        scheerCount += 1
        partyList['cpc'] += 1
        articleCopy = articleCopy.replace('andrew scheer','')
    if "andrew" in articleCopy and scheerCount == 0:
        scheerCount += 1
        partyList['cpc'] += 1
        articleCopy = articleCopy.replace('andrew','')
    if "scheer" in articleCopy and scheerCount == 0:
        scheerCount += 1
        partyList['cpc'] += 1
        articleCopy = articleCopy.replace('scheer','')

    if "jagmeet singh" in articleCopy and singhCount == 0:
        singhCount += 1
        partyList['ndp'] += 1
        articleCopy = articleCopy.replace('jagmeet singh','')
    if "jagmeet" in articleCopy and singhCount == 0:
        singhCount += 1
        partyList['ndp'] += 1
        articleCopy = articleCopy.replace('jagmeet','')
    if "singh" in articleCopy and singhCount == 0:
        singhCount += 1
        partyList['ndp'] += 1
        articleCopy = articleCopy.replace('singh','')
    
    articles = nlp(articleCopy)
    tokens = [i.text.strip() for i in articles]
    for token in tokens:
        if token in partiesObj['lib']:
            partyList['lib'] += 1  
        if token in partiesObj['cpc']:
            partyList['cpc'] += 1
        if token in partiesObj['ndp']:
            partyList['ndp'] += 1

    return partyList

news_tags = news2.copy()

lib = []
cpc = []
ndp = []
parties = []

for article in news_tags.Full_text:
    article = article.lower()
    tag = tagNews(article)

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

news_tags['lib'] = lib
news_tags['cpc'] = cpc
news_tags['ndp'] = ndp

lib = (news_tags['lib'] == 1)
cpc = (news_tags['cpc'] == 1)
ndp = (news_tags['ndp'] == 1)

news_tags = news_tags[lib | cpc | ndp]

news_tags.to_csv('./data/news/combined_news_csv.csv')