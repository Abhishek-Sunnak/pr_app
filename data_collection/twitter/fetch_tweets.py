import os
import json
import requests
import csv
import datetime
from requests_oauthlib import OAuth1

API_KEY = 'ru0TKZfX8TGlKrQgoEupRhX19'
API_SECRET = 'EYe3A8A7CD2NgB5B7X6XEJEuZK4U7KBCj4dB6U1D7FDNBwgJwY'
ACCESS_TOKEN = '40521095-3xmfiBYTzCFidrtG5FZdwK1ab201GBj1Ei63dr5FK'
ACCESS_TOKEN_SECRET = 'v5leAUvTSh2pt4puWJp91Pyb5MrL4aF15DqgO6FaW8nau'

auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
max_id = 0
tweetCount = 0
maxTweets = 10000000
searchQuery = ''

with open('./data/twitter/since_id.txt', 'r') as file:
  since_id = int(file.readline())

with open('./data/keywords/canadian_elections_tw.csv', 'r') as file:
    queries = csv.reader(file)
    next(queries, None)
    texts = ''
    hashTags = ''
    for q in queries:
        if q[2] == 'Query':
            texts += q[1]+ '%20OR%20'
        if q[2] == 'Hashtags':
            hashTags += '%23'+q[1]+'%20OR%20'
    searchQuery = searchQuery + texts
    searchQuery = searchQuery + hashTags

counter = 0
while tweetCount < maxTweets:
  if (max_id <= 0):
      if not since_id:
          new_tweets = requests.get('https://api.twitter.com/1.1/search/tweets.json?q={}&result_type=mixed&count=100&tweet_mode=extended&lang=en'.format(searchQuery), auth=auth)
      else:
          new_tweets = requests.get('https://api.twitter.com/1.1/search/tweets.json?q={}&result_type=mixed&count=100&tweet_mode=extended&lang=en&since_id={}'.format(searchQuery,since_id), auth=auth)
  else:
      if not since_id:
          new_tweets = requests.get('https://api.twitter.com/1.1/search/tweets.json?q={}&result_type=mixed&count=100&tweet_mode=extended&lang=en&max_id={}'.format(searchQuery, str(max_id - 1)), auth=auth)
      else:
          new_tweets = requests.get('https://api.twitter.com/1.1/search/tweets.json?q={}&result_type=mixed&count=100&tweet_mode=extended&lang=en&max_id={}&since_id={}'.format(searchQuery, str(max_id - 1), since_id), auth=auth)            
  if not new_tweets:
      # print("No more tweets found")
      break
  statuses = new_tweets.json()['statuses']
  #save to csv
  fieldNames = ['created_at','id','id_str','full_text','truncated','display_text_range','entities','extended_entities','metadata','source','in_reply_to_status_id','in_reply_to_status_id_str','in_reply_to_user_id','in_reply_to_user_id_str','in_reply_to_screen_name','user','geo','coordinates','place','contributors','retweeted_status','is_quote_status','quoted_status_id','quoted_status_id_str','quoted_status','retweet_count','favorite_count','favorited','retweeted','possibly_sensitive','lang']

  with open("./data/twitter/twitter_canada_"+str(datetime.datetime.today()).split()[0]+".csv", 'a', encoding='utf8', newline='') as output_file:
      fc = csv.DictWriter(output_file, fieldnames=fieldNames, delimiter=",")
      if counter == 0:
          fc.writeheader()
      fc.writerows(statuses)

  tweetCount += len(statuses)
  counter += 1
  # print("Downloaded {0} tweets".format(tweetCount))
  max_id = statuses[-1]['id']
  next_run_since = statuses[0]['id']
  # print(max_id, 'last max_id saved')
  # print(next_run_since, 'since_id for next run.......')

  with open('./data/twitter/since_id.txt', 'w') as file:
    file.write(next_run_since)