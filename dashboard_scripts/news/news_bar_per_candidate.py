import pandas as pd
import json

df = pd.read_csv('./data/news/combined_news_csv.csv')

df_lib = df[df['lib'] == 1]
df_cpc = df[df['cpc'] == 1]
df_ndp = df[df['ndp'] == 1]

def publications_per_party(d, publications):
    data = []
    bias_labels = {
        '__label__least': 'No Bias',
        '__label__left': 'Left',
        '__label__left-center': 'Left Centric',
        '__label__right': 'Right',
        '__label__right-center': 'Right Centric'
    }
    newdf = d[['Provider', 'Bias', 'Headline']].groupby(['Provider', 'Bias']).count()
    newdf2 = d[['Provider', 'Headline']].groupby(['Provider']).count()
    newdf = newdf.loc[publications]
    newdf2 = newdf2.loc[publications]
    
    for index, row in newdf2.iterrows():
        temp_df = newdf.loc[index]
        item = {
            'publication': index,
            'data': int(row['Headline'])
        }
        for key in bias_labels.keys():
            item[bias_labels[key]] = 0
        for bias, row in temp_df.iterrows():
            item[bias_labels[bias]] = int(row['Headline'])
        data.append(item)
    return data

df_publication = df[['Provider', 'Headline']].groupby('Provider').count().sort_values(['Headline'], ascending=False).head(5)
top_publications = list(df_publication.index)
publs_part = {
    'LPC': publications_per_party(df_lib, top_publications),
    'CPC': publications_per_party(df_cpc, top_publications),
    'NDP': publications_per_party(df_ndp, top_publications),
    'all': publications_per_party(df, top_publications),
}

with open('./dashboard/public/static/newsBarPerCandidate.json', 'w') as file:
    json.dump(publs_part, file)