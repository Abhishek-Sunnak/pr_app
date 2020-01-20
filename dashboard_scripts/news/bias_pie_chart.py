import pandas as pd
import json

df = pd.read_csv('./data/news/combined_news_csv.csv')

bias_keys = ['__label__left', '__label__left-center', '__label__least', '__label__right-center', '__label__right']
bias_labels = {
    '__label__left': 'Left',
    '__label__left-center': 'Left Centric',
    '__label__least': 'No Bias',
    '__label__right-center': 'Right Centric',
    '__label__right': 'Right'
}

df_lib = df[df['lib'] == 1]
df_cpc = df[df['cpc'] == 1]
df_ndp = df[df['ndp'] == 1]

def biasPieChart(d):
    data = []
    sum_data = len(d)
    groupedData = d[['Headline', 'Bias']].groupby('Bias').count()

    for bias_key in bias_keys:
        item = {}
        value = groupedData.loc[bias_key]['Headline']
        item['value'] = round(value * 100 / sum_data)
        item['bias'] = bias_labels[bias_key]
        data.append(item)
    return data

biasPie = {}
biasPie['all'] = biasPieChart(df)
biasPie['CPC'] = biasPieChart(df_cpc)
biasPie['NDP'] = biasPieChart(df_ndp)
biasPie['LPC'] = biasPieChart(df_lib)

with open('./dashboard/public/static/biasPieChart.json', 'w') as file:
    json.dump(biasPie, file)