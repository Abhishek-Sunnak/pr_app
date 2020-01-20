import pandas as pd

df = pd.read_csv('./data/poll/province_poll_data.csv')
df['Date'] = df['Time'].apply(lambda datestring: pd.to_datetime(datestring))
newdf = df[df['Date'] >= pd.to_datetime('March 2018')]
newdf['Date'] = newdf['Date'].apply(lambda time: time.strftime('%b%y'))
newdf[['Date','Conservative', 'NDP', 'Liberals', 'Province', 'Time']].to_json('./dashboard/public/static/province_poll_data.json', orient='records')
