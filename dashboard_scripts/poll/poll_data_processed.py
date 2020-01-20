import pandas as pd

df = pd.read_csv('./data/poll/province_poll_data.csv')
df['Date'] = df['Time'].apply(lambda datestring: pd.to_datetime(datestring))

national = df[df['Province'] == 'National']
national = national.sort_values('Date', ascending=False)
national = national.reset_index()
lastDate = national['Date'][0]

df = df[df['Date'] == lastDate]

def get_max(row):
    if row['Liberals'] > row['NDP'] and row['Liberals'] > row['Conservative']:
        return 'Liberals'
    elif row['Conservative'] > row['NDP'] and row['Conservative'] > row['Liberals']:
        return 'Conservative'
    else:
        return 'NDP'
df['Max'] = df.apply(get_max, axis=1)

columns = ['Conservative', 'Liberals', 'NDP', 'Province', 'Max']
df = df[columns]

df.to_json('./dashboard/public/static/poll_data_processed.json', orient='records')