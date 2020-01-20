import pandas as pd
from datetime import datetime

df = pd.read_csv('./data/twitter/cleaned.csv')
df = df.sort_values(by=['created_at'], ascending=True)

def get_sentiment(sentiment):
    if(sentiment == 'Positive'):
        return 1
    elif sentiment == 'Neutral':
        return 0
    else:
        return -1
df['sentiment'] = df['Final_Sentiment'].apply(get_sentiment)

df["Week"]=df["created_at"].apply(lambda x:"2019-W"+str(datetime.strptime(x, '%a %b %d %X %z %Y').isocalendar()[1]))
df["Date"]=df["Week"].apply(lambda x: datetime.strptime(x + '-1', "%Y-W%W-%w"))
df["Date_processed"]=df["Date"].apply(lambda x: x.strftime('%d-%b'))
df = df.sort_values(by=['Date'], ascending=True)
df["sentiment"] = df["sentiment"] * 5

def reshape_data(df,party="National"):
    National = df[["sentiment","Date"]].groupby('Date').mean()
    National.reset_index(inplace=True)
    National.columns = ["Date","National"]
    df2 = df[["sentiment","Date","region"]].groupby(['region','Date']).mean()
    df2.reset_index(inplace=True)
    Regional = df2.pivot(columns='region', values='sentiment')
    Regional["Date"]=df2["Date"]
    Regional = Regional.groupby(['Date']).sum()
    Regional.reset_index(inplace=True)
    Overall = National.merge(Regional,on="Date",how='left')

    Overall = Overall.fillna(value=0)
    Overall["Party"]=party
    return Overall

df["Week"]=df["created_at"].apply(lambda x:"2019-W"+str(datetime.strptime(x, '%a %b %d %X %z %Y').isocalendar()[1]))
df["Date"]=df["Week"].apply(lambda x: datetime.strptime(x + '-1', "%Y-W%W-%w"))
df["Date_processed"]=df["Date"].apply(lambda x: x.strftime('%d-%b'))
df = df.sort_values(by=['Date'], ascending=True)
All_party= reshape_data(df)
CPC = reshape_data(df[df.cpc==1],party="CPC")
LIB = reshape_data(df[df.lib==1],party="LPC")
NDP = reshape_data(df[df.ndp==1],party="NDP")

Final = pd.concat([All_party, CPC, LIB, NDP], ignore_index=True)

Final = Final.fillna(value=0)
Final = Final.sort_values(by=['Date'], ascending=True)
Final["Date2"]=Final["Date"].apply(lambda x: x.strftime('%d-%b-%Y'))
Final.index = range(len(Final))

final_dict=dict()
final_array=list()
province_list=['Alberta', 'Atlantic', 'British Columbia','National', 'Ontario','Praires', 'Quebec']
for index in range(len(Final)):
    for province in province_list:
        final_array.append({"province": province,"time": Final["Date2"][index],
             "number": float(Final[province][index]),"party": Final["Party"][index]})
import json
with open('./dashboard/public/static/tweets_sentiment_distribution.json', 'w') as outfile:
    json.dump(final_array, outfile) 
