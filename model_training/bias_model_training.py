#!/usr/bin/env python
# coding: utf-8

import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import pandas as pd
import glob
import re
import datetime
import fastText
import os
from html.parser import HTMLParser
import io
import xml.etree.ElementTree
import re
import csv
import nltk
from bs4 import BeautifulSoup
import itertools
import emoji
from sklearn.model_selection import train_test_split
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import pandas as pd
import seaborn as sns
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import sys
import optparse

optparser = optparse.OptionParser()
optparser.add_option("-a", "--articles", dest="articles", default="articles-training-bypublisher-20181122.xml", help="Name of Training Data by Publisher (XML File)")
optparser.add_option("-t", "--target", dest="target", default="ground-truth-training-bypublisher-20181122.xml", help="Name of Target Data by Publisher (XML File)")
optparser.add_option("-m", "--model", dest="model", default="model-bias", help="Name of Model to be saved")
(opts, _) = optparser.parse_args()


path = "./data/training_data/"
articlesfile = path+ opts.articles
articles_target = path+ opts.target
moel_path = "./data/models/"

model_name = opts.model



#Define functions for Text Pre-processing and Parsing
txt_tospace1 = re.compile('&#160;')

def cleantext(text):
    '''Clean the text extracted from XML.'''
    text = text.replace("&amp;", "&")
    text = text.replace("&gt;", ">")
    text = text.replace("&lt;", "<")
    text = text.replace("<p>", " ")
    text = text.replace("</p>", " ")
    text = text.replace(" _", " ")
    text = text.replace("–", "-")
    text = text.replace("”", "\"")
    text = text.replace("“", "\"")
    text = text.replace("’", "'")

    text, _ = txt_tospace1.subn(' ', text)
    return text

class MyHTMLParser(HTMLParser):

    def __init__(self):
        kwargs = {}
        HTMLParser.__init__(self, **kwargs)
        self.ignore = False
        self.data = []
        self.p = []

    def finishp(self):
        if len(self.p) > 0:
            self.data.append(self.p)
            self.p = []

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        if tag in ['script', 'style']:
            self.ignore = True
        elif tag in ['p', 'br']:
            self.finishp()
        # any tags that need to get repalced by space?
        # elif tag in ['???']:
        #     self.p.append(" ")

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        if tag in ['script', 'style']:
            self.ignore = False
        elif tag in ['p', 'br']:
            self.finishp()
        # any tags that need to get repalced by space?
        # elif tag in ['???']:
        #     self.p.append(" ")

    def handle_startendtag(self, tag, attrs):
        # print("Encountered a startend tag:", tag)
        if tag in ['p', 'br']:
            self.finishp()

    def handle_data(self, data):
        # print("Encountered some data  :", data)
        if not self.ignore:
            self.p.append(data)

    def close(self):
        HTMLParser.close(self)
        self.finishp()

    def reset(self):
        HTMLParser.reset(self)
        self.data = []
        self.p = []

    def cleanparagraph(self, text):
        """
        How to do basic cleaning up of the text in each paragraph
        :return:
        """
        text = cleantext(text)
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        text = ' '.join(text.split()).strip()
        return text

    def paragraphs(self):
        """
        Convert collected data to paragraphs
        """
        pars = []
        for par in self.data:
            if len(par) > 0:
                text = self.cleanparagraph(''.join(par)).strip()
                if text:
                    pars.append(text)
        return pars
    
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

def comb_list(text):
    return ''.join(text)

def cleantext(text):
    '''Clean the text extracted from XML.'''
    text = text.replace("&amp;", "&")
    text = text.replace("&gt;", ">")
    text = text.replace("&lt;", "<")
    text = text.replace("<p>", " ")
    text = text.replace("</p>", " ")
    text = text.replace(" _", " ")
    text = text.replace("–", "-")
    text = text.replace("”", "\"")
    text = text.replace("“", "\"")
    text = text.replace("’", "'")
    text = text.replace("\\\'","'")
    text = text.replace("…",".")
    
    
    text, _ = txt_tospace1.subn(' ', text)
    return text

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


# Code to Train the Model

training_data_path =path+'news.train'
validation_data_path =path+'news.validation'

def train(lr=0.01,epochs=40,wordgrams=2,dim=150,thread=32,model_name="model-en",loss="softmax"):
    print('Training start')
    try:
        hyper_params = {"lr": lr,
                        "epoch": epochs,
                        "wordNgrams": wordgrams,
                        "dim": dim,
                        "thread": thread,
                        "loss":loss
                       }     
                               
        print(str(datetime.datetime.now()) + ' START=>' + str(hyper_params) )

        # Train the model.
        model = fastText.train_supervised(input=training_data_path, **hyper_params)
        print("Model trained with the hyperparameter \n {}".format(hyper_params))

        # CHECK PERFORMANCE
        print(str(datetime.datetime.now()) + '\nTraining complete.\n' + str(hyper_params) )
        
        model_acc_training_set = model.test(training_data_path)
        model_acc_validation_set = model.test(validation_data_path)
        
        # DISPLAY ACCURACY OF TRAINED MODEL
        text_line = str(hyper_params) + ",accuracy:" + str(model_acc_training_set[1])  + ", validation:" + str(model_acc_validation_set[1]) + '\n' 
        print(text_line)
        
        #quantize a model to reduce the memory usage
        model.quantize(input=training_data_path, qnorm=True, retrain=True, cutoff=100000)
        
        print("Model is quantized!!")
        model.save_model(os.path.join(model_path,model_name + ".ftz"))                

    except Exception as e:
        print('Exception during training: ' + str(e) )


tree = ET.iterparse(articlesfile)

tree = ET.iterparse(articlesfile)
i = 0
nprocessed = 0
nerror = 0
article_data = pd.DataFrame(columns=['id', 'published-at', 'text', 'Title'])
for event, element in tree:
    if element.tag == "article":
        if i%50000==0:
            print(i)
        i+=1
        attrs = element.attrib
        articleid = attrs['id']
        published = attrs.get("published-at")
        # get the XML and store it in a dictionary as "xml"
        xml = ET.tostring(element, encoding="utf-8", method="xml").decode()
        article = {
            'id': articleid,
            'xml': xml,
            'published-at': published,
            'et': element
        }
        parser = MyHTMLParser()
        parser.reset()
        parser.feed(article['xml'])
        parser.close()
        pars = parser.paragraphs()
        article["text"] = pars
        art = ET.parse(io.StringIO(article["xml"])).getroot()
        article["Title"] = art.attrib["title"]
        del article['et']
        del article['xml']
        article_data = article_data.append(pd.DataFrame.from_dict(article,orient='index').T)

#Save as csv File 
article_data.to_csv(path+"articles_processed.csv")

i = 0
tree = ET.iterparse(articles_target)
nprocessed = 0
nerror = 0
article_target_data = pd.DataFrame(columns=['id', 'hyperpartisan', 'bias', 'url', 'labeled-by'])
for event, element in tree:
    if element.tag == "article":
        attrs = element.attrib
        article_target_data = article_target_data.append(pd.DataFrame.from_dict(element.attrib,orient='index').T)
        i+=1
        if (i%10000==0):
            print(i)
            

target_data = article_target_data[['id', 'hyperpartisan', 'bias', 'url', 'labeled-by']]
target_data["id"] = pd.to_numeric(target_data["id"])

read_data = read_data[['id', 'published-at', 'text', 'Title']]
article_data_full = read_data.merge(target_data,on="id")


# In[4]:


id=list()
clean_text=list()
for i in range(len(article_data_full)):
    id.append(i)
    clean_text.append(tweet_cleaning_for_sentiment_analysis(article_data_full["text"][i]))
    if i%5000==0:
        print(i)
    i+=1
    
article_data_full["Text_clean"]=clean_text
article_data_full = article_data_full.sort_values(by=['id'])
article_data_full=article_data_full.drop_duplicates()
article_data_full.to_csv(path+"News_full_train.csv")


# Split into training and Validation Data

train, test = train_test_split(news_data, test_size=0.2)

train.to_csv(path+"train.csv",index=False)

test.to_csv(path+"val.csv",index=False)


# Convert Data Format to train FastText Model

csv.field_size_limit(100000000)
def transform_instance(row):
    cur_row = []
    #Prefix the index-ed label with __label__
    label = "__label__" + row[3]  
    cur_row.append(label)
    cur_row.extend(nltk.word_tokenize(tweet_cleaning_for_sentiment_analysis(row[0].lower())))
    return cur_row

def preprocess(input_file, output_file, keep=1):
    i=0
    with open(output_file, 'w') as csvoutfile:
        csv_writer = csv.writer(csvoutfile, delimiter=' ', lineterminator='\n')
        with open(input_file, 'r', newline='', encoding='latin1') as csvinfile: #,encoding='latin1'
            csv_reader = csv.reader(csvinfile, delimiter=',', quotechar='"')
            for row in csv_reader:
                if row[0]!='':
                    if row[3]!="MIXED" and row[3].upper() in ['RIGHT','LEAST','LEFT',"LEFT-CENTER","RIGHT-CENTER"] and row[3]!='':
                        row_output = transform_instance(row)
                        csv_writer.writerow(row_output )
                    # print(row_output)
                i=i+1
                if i%10000 ==0:
                    print(i)
            
# Preparing the training dataset        
preprocess(path+'train.csv', path + 'news.train')

# # Preparing the validation dataset
preprocess(path+'val.csv', path + 'news.validation')

# Train your model.
train(lr=0.01,epochs=40,wordgrams=2,dim=20,model_name=model_name)
