import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import numpy as np
import datetime

def get_timestamp(time):
    if time == 'Present':
        time = '2019-04-14'
    return pd.to_datetime(time)

def get_leadermeter_content():
    leader_meter = requests.get('https://canopy.cbc.ca/live/leader_meter/data')
    leader_content = leader_meter.text
    leader_data = json.loads(leader_content, strict=False)
    return leader_data

def clean_dataframe(df):
    df = df.replace('', np.nan, regex=True)
    cols_needed = ['cpcapp', 'cpcdis', 'cpcdk', 'lpcapp', 'lpcdis', 
                'lpcdk', 'ndpapp', 'ndpdis', 'ndpdk', 'finish', 
                'polllink', 'samplesize']
    df = df[cols_needed].dropna()
    return df

def filter_dataframe(df, prev_date):
    df['time'] = df['finish'].apply(get_timestamp)
    df = df[df['time'] > pd.to_datetime(prev_date)]
    df['time'] = df['time'].apply(lambda time: time.strftime('%Y-%m'))
    cols = ['cpcapp', 'cpcdis', 'cpcdk', 'lpcapp', 'lpcdis', 'lpcdk', 'ndpapp', 'ndpdis', 'ndpdk']
    for col in cols:
        df[col] = df[col].apply(int)
    df = df.replace(0, np.nan)    
    df = df[['cpcapp', 'cpcdis', 'cpcdk', 'lpcapp', 'lpcdis', 'lpcdk', 'ndpapp', 'ndpdis', 'ndpdk', 'time']]
    return df

def process_dataframe(df, prev_date, curr_date):
    idx = pd.date_range(prev_date, curr_date, freq='MS')
    df['time'] = df['time'].apply(get_timestamp)
    df = df.groupby('time').mean().reset_index()
    df.index = pd.DatetimeIndex(df['time'])
    df = df[['cpcapp', 'cpcdis', 'cpcdk', 'lpcapp', 'lpcdis', 'lpcdk', 'ndpapp', 'ndpdis', 'ndpdk']].reindex(idx, method='backfill')
    df['finish'] = idx
    df['finish'] = df['finish'].apply(lambda time: time.strftime('%b%y'))
    return df

now = datetime.datetime.now()
curr_year = now.year
prev_year = curr_year - 1
month = now.month - 1
month = '{:02d}'.format(month)
curr_date = str(curr_year) + '-' + month + '-01'
prev_date = str(prev_year) + '-' + month + '-01'

leader_data = get_leadermeter_content()
df = pd.DataFrame(leader_data)
df = clean_dataframe(df)
df = filter_dataframe(df, prev_date)
df = process_dataframe(df, prev_date, curr_date)
df.to_json('./dashboard/public/static/leadermeter-polling-data.json', orient='records')
