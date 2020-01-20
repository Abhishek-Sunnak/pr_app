#!/usr/bin/env python
# coding: utf-8

import sys
import os
import nltk
nltk.download('punkt')
import csv
import datetime
from bs4 import BeautifulSoup
import re
import itertools
import emoji
import pandas as pd
import seaborn as sns
import fastText
import optparse

optparser = optparse.OptionParser()
optparser.add_option("-p", "--path", dest="path", default="./data/training_data/", help="Path of training Datasets")
optparser.add_option("-a", "--modelA", dest="modelA", default="model-en5", help="Name of 1st Model to be saved")
optparser.add_option("-b", "--modelB", dest="modelB", default="model-en3", help="Name of 2nd Model to be saved")
optparser.add_option("-c", "--modelC", dest="modelC", default="model-en_org2", help="Name of 3rd Model to be saved")
(opts, _) = optparser.parse_args()

path = opts.path
training_data_path =path+'uptweets.train'
validation_data_path =path+'tweets.validation'
moel_path = "./data/models/"
model_name = opts.model

# ## DATA CLEANING
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
        "how'd":"how would","how'll":"how will","how're":"how are","how's":"how is","I'd":"I would",
        "I'll":"I will","I'm":"I am","I'm'a":"I am about to","I'm'o":"I am going to","isn't":"is not",
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
    
    #Removal of hastags/account
    tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", tweet).split())
    
    #Removal of address
    tweet = ' '.join(re.sub("(\w+:\/\/\S+)", " ", tweet).split())
    
    #Removal of Punctuation
    tweet = ' '.join(re.sub("[\.\,\!\?\:\;\-\=]", " ", tweet).split())
    
    #Lower case
    tweet = tweet.lower()
    
    #CONTRACTIONS source: https://en.wikipedia.org/wiki/Contraction_%28grammar%29
    CONTRACTIONS = load_dict_contractions()
    tweet = tweet.replace("’","'")
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


def transform_instance(row):
    cur_row = []
    #Prefix the index-ed label with __label__
    label = "__label__" + row[1]  
    cur_row.append(label)
    cur_row.extend(nltk.word_tokenize(tweet_cleaning_for_sentiment_analysis(row[2].lower())))
    return cur_row


def preprocess(input_file, output_file, keep=1):
    i=0
    with open(output_file, 'w') as csvoutfile:
        csv_writer = csv.writer(csvoutfile, delimiter=' ', lineterminator='\n')
        with open(input_file, 'r', newline='', encoding='latin1') as csvinfile: #,encoding='latin1'
            csv_reader = csv.reader(csvinfile, delimiter=',', quotechar='"')
            for row in csv_reader:
                if row[1]!='':
                    if row[1]!="MIXED" and row[1].upper() in ['POSITIVE','NEGATIVE','NEUTRAL'] and row[2]!='':
                        row_output = transform_instance(row)
                        csv_writer.writerow(row_output )
                    # print(row_output)
                i=i+1
                if i%10000 ==0:
                    print(i)

def transform_instance_val(row):
    cur_row = []
    #Prefix the index-ed label with __label__
    label = "__label__" + row[4]  
    cur_row.append(label)
    cur_row.extend(nltk.word_tokenize(tweet_cleaning_for_sentiment_analysis(row[2].lower())))
    return cur_row


def preprocess_val(input_file, output_file, keep=1):
    i=0
    with open(output_file, 'w') as csvoutfile:
        csv_writer = csv.writer(csvoutfile, delimiter=' ', lineterminator='\n')
        with open(input_file, 'r', newline='', encoding='latin1') as csvinfile: #,encoding='latin1'
            csv_reader = csv.reader(csvinfile, delimiter=',', quotechar='"')
            for row in csv_reader:
                if row[4]!="MIXED" and row[4].upper() in ['POSITIVE','NEGATIVE','NEUTRAL'] and row[2]!='':
                    row_output = transform_instance_val(row)
                    csv_writer.writerow(row_output )
                    # print(row_output)
                i=i+1
                if i%10000 ==0:
                    print(i)

# ## UPSAMPLING
def upsampling(input_file, output_file, ratio_upsampling=1):
    # Create a file with equal number of tweets for each label
    #    input_file: path to file
    #    output_file: path to the output file
    #    ratio_upsampling: ratio of each minority classes vs majority one. 
    
    i=0
    counts = {}
    dict_data_by_label = {}

    # GET LABEL LIST AND GET DATA PER LABEL
    with open(input_file, 'r', newline='') as csvinfile: 
        csv_reader = csv.reader(csvinfile, delimiter=',', quotechar='"')
        for row in csv_reader:
            counts[row[0].split()[0]] = counts.get(row[0].split()[0], 0) + 1
            if not row[0].split()[0] in dict_data_by_label:
                dict_data_by_label[row[0].split()[0]]=[row[0]]
            else:
                dict_data_by_label[row[0].split()[0]].append(row[0])
            i=i+1
            if i%10000 ==0:
                print("read" + str(i))

    # FIND MAJORITY CLASS
    majority_class=""
    count_majority_class=0
    for item in dict_data_by_label:
        if len(dict_data_by_label[item])>count_majority_class:
            majority_class= item
            count_majority_class=len(dict_data_by_label[item])  
    
    # UPSAMPLE MINORITY CLASS
    data_upsampled=[]
    for item in dict_data_by_label:
        data_upsampled.extend(dict_data_by_label[item])
        if item != majority_class:
            items_added=0
            items_to_add = count_majority_class - len(dict_data_by_label[item])
            while items_added<items_to_add:
                data_upsampled.extend(dict_data_by_label[item][:max(0,min(items_to_add-items_added,len(dict_data_by_label[item])))])
                items_added = items_added + max(0,min(items_to_add-items_added,len(dict_data_by_label[item])))

    # WRITE ALL
    i=0

    with open(output_file, 'w') as txtoutfile:
        for row in data_upsampled:
            txtoutfile.write(row+ '\n' )
            i=i+1
            if i%10000 ==0:
                print("writer" + str(i))

# ## Model TRAINING

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
        print(str(datetime.datetime.now()) + 'Training complete.' + str(hyper_params) )
        
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


# ## DATA PROCESSING

# #### Import GOP Tweets Data
data1 = pd.read_csv(path+'Sentiment.csv')
data1 = data1[["id","sentiment","text"]]
data1["sentiment"] = data1["sentiment"].str.upper()

# #### Import Semeval Tweets Data

data2 = pd.read_csv(path+'SemEval2017-task4-dev.subtask-A.english.INPUT.txt', sep="\t", header=None)
data2.columns = ["id", "sentiment", "text", "etc"]
data2["sentiment"] = data2["sentiment"].str.upper()
data2 = data2.drop(["etc"], axis=1)

data3 = pd.read_csv(path+'betsentiment-EN-tweets-sentiment-teams.csv',encoding='latin1')
data3 = data3[["tweet_id","sentiment","tweet_text"]]
data3.columns = ["id", "sentiment", "text"]

# ### Combine All the Dataframes
data_comb = data1.append([data2, data3])
data_comb = data_comb.dropna()


data_comb.to_csv(path +"Combined_tweets.csv",index=False)
data_comb = pd.read_csv(path+'Combined_tweets.csv',encoding='latin1')
data_comb = data_comb.dropna()
data_comb.to_csv(path +"Combined_tweets.csv",index=False)
            
# Preparing the training dataset        
preprocess(path+'Combined_tweets.csv', path+'tweets.train')

# # Preparing the validation dataset
preprocess_val(path+'betsentiment-EN-tweets-sentiment-players.csv', path+'tweets.validation')


# Upsampling the Training Data
upsampling( path+'tweets.train',path+'uptweets.train')
# No need to upsample for the validation set. As it does not matter what validation set contains.

# Model Training
train(lr=0.05,epochs=20,wordgrams=4,dim=20,model_name=opts.modelA)

train(lr=0.005,epochs=10,wordgrams=2,dim=150,thread=64,model_name=opts.modelB)

# ### Training without upsampling
training_data_path =path+'tweets.train'
validation_data_path =path+'tweets.validation'
train(lr=0.005,epochs=10,wordgrams=2,dim=200,thread=64,loss="softmax",model_name=opts.modelC)
