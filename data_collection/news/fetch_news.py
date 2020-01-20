from azure.cognitiveservices.search.newssearch import NewsSearchAPI
from msrest.authentication import CognitiveServicesCredentials
import newspaper
from newspaper import Article
import pandas as pd
import datetime
import glob
import nltk
nltk.download('gutenberg')

from pprint import pprint
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
from nltk.corpus import gutenberg
 
subscription_key = "8a4ebe4976ee4e24935b3a1ae0a56cfb"
search_term = "Canada Elections"

client = NewsSearchAPI(CognitiveServicesCredentials(subscription_key))

def Create_news_df(news_result):
  news_df=pd.DataFrame(columns=["Headline","URL","Category","Description",
                            "Date_published","Provider"])
  for i in range(len(news_result.value)):
    if news_result.value:
      news = news_result.value[i]
      new_dict=dict()
      new_dict={"Headline":news.name,"URL":news.url,"Category":news.category,
            "Description":news.description,"Date_published":news.date_published,
            "Provider":news.provider[0].name,"Full_text":"Empty"}
      df=pd.DataFrame([new_dict],columns=new_dict.keys())
      news_df=news_df.append(df,ignore_index=True)
  return news_df

#Get News about The Canadian Election

keywords = pd.read_excel('./data/keywords/news.xlsx', 'Canadian_Elections')['Search_Queries'].tolist()
#create a new empty dataframe
combined_df=pd.DataFrame(columns=["Headline","URL","Category","Description",
                              "Date_published","Provider","Full_text"])

for key in range(len(keywords)):
  news_result = client.news.search(query=keywords[key], #market="en-CA",
                                category="Politics", count=50)
  
  combined_df=combined_df.append(Create_news_df(news_result),ignore_index=True)
  
  news_result = client.news.search(query=search_term, #market="en-CA",
                                category="Politics", count=50,offset=50)
  
  combined_df=combined_df.append(Create_news_df(news_result),ignore_index=True)
  
  news_result = client.news.search(query=search_term, #market="en-CA",
                                category="Politics", count=50,offset=100)

  combined_df=combined_df.append(Create_news_df(news_result),ignore_index=True)
    
print("Collected News")

combined_df_dedup=combined_df.drop_duplicates()
combined_df_dedup.index=range(len(combined_df_dedup))

url_list=list(combined_df_dedup["URL"])

s_list=list()
art_text=list()

for i in range(len(url_list)):
  url=url_list[i]
  try:
    article = Article(url)
    article.download()
    article.parse()
    art_text.append(article.text)
    s_list.append(i)
    combined_df_dedup.iloc[i, combined_df_dedup.columns.get_loc('Full_text')] = article.text
  except Exception:
    continue  

print("Collected Full News Text")

combined_df_dedup.to_csv("./data/news/Can_News_csv_"+str(datetime.datetime.today()).split()[0]+".csv")

print("Done")

combined_df_dedup_canada=combined_df_dedup

#News Api
from newsapi import NewsApiClient
import pandas as pd
# Init
newsapi = NewsApiClient(api_key='995950f89be24311a88c46457899d3a0')


def Create_news_df_2(all_articles):
  all_articles2=all_articles["articles"]
  
  news_df=pd.DataFrame(columns=["Headline","URL","Category","Description",
                            "Date_published","Provider"])
  for i in range(len(all_articles2)):
    news = all_articles2[i]
    new_dict=dict()
    new_dict={"Headline":news["title"],"URL":news["url"],"Category":"Empty",
              "Description":news['description'],"Date_published":news["publishedAt"],
              "Provider":news["source"]["name"],"Full_text":"Empty"}
    df=pd.DataFrame([new_dict],columns=new_dict.keys())
    news_df=news_df.append(df,ignore_index=True)
  return news_df

# keywords=list(pd.read_csv("./data/Keywords/Canadian Elections.csv")["Search_Queries"])
keywords = pd.read_excel('./data/keywords/news.xlsx', 'Canadian_Elections')['Search_Queries'].tolist()
news_df=pd.DataFrame(columns=["Headline","URL","Category","Description",
                              "Date_published","Provider"])


start_date = (datetime.datetime.now() + datetime.timedelta(-28)).strftime('%Y-%m-%d')
end_date = (datetime.datetime.now()).strftime('%Y-%m-%d')


for key in range(len(keywords)):
  for page in range(1,6):
    all_articles = newsapi.get_everything(q=keywords[key],
#                                       sources='bbc-news,the-verge',
#                                       domains='bbc.co.uk,techcrunch.com',
                                      from_param=start_date,
                                      to='2019-02-25',
                                      language='en',
                                      sort_by='relevancy',
                                      page=page)
    news=Create_news_df_2(all_articles)
    news_df=news_df.append(news,ignore_index=True)      

combined_df_dedup=news_df.drop_duplicates()
combined_df_dedup.index=range(len(combined_df_dedup))

url_list=list(combined_df_dedup["URL"])

print("Collected News")

s_list=list()
art_text=list()

for i in range(len(url_list)):
  url=url_list[i]
  try:
    article = Article(url)
    article.download()
    article.parse()
    art_text.append(article.text)
    s_list.append(i)
    combined_df_dedup.iloc[i, combined_df_dedup.columns.get_loc('Full_text')] = article.text
  except Exception:
      continue

print("Collected Full News Text")

combined_df_dedup.to_csv("./data/news/Can_News2_csv_"+str(datetime.datetime.today()).split()[0]+".csv")

print("Done")