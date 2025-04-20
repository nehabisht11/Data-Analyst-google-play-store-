#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import datetime as dt
import pytz
import plotly.express as px
import streamlit as st

def main():
    app = pd.read_csv('google playstore data.csv')

    app = app[app['Installs'].str.contains(r'\d', regex=True, na=False)]
    app['Installs'] = app['Installs'].str.replace('[,+]', '', regex=True).astype(int)
    app = app[~app['Rating'].isna()]

    app_filter = app[
        (app['Category'].str.contains('GAME')) &
        (app['Installs'] > 50000) &
        (app['Rating'] > 3.5)
    ]

    def convert_size(x):
        x = str(x).lower()
        if 'k' in x:
            return float(x.replace('k', '')) / 1024
        elif 'm' in x:
            return float(x.replace('m', ''))
        else:
            return None

    app_filter['Size'] = app_filter['Size'].apply(convert_size)

    grouped = app_filter.groupby(['App', 'Size']).agg({
        'Installs': 'sum',
        'Rating': 'mean'
    }).reset_index()

    IST = pytz.timezone('Asia/Kolkata')
    current_time = dt.datetime.now(IST).time()
    start_time = dt.time(17, 0)
    end_time = dt.time(19, 0)

    if start_time <= current_time <= end_time:
        fig = px.scatter(
            grouped,
            x='Size',
            y='Rating',
            size='Installs',
            color='Installs',
            hover_name='App',
            title='Bubble Chart: App Size vs Rating (Games Category)',
            labels={'Size': 'App Size (MB)', 'Rating': 'Average Rating'},
            size_max=60,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        print('The chart is only available between 5 PM and 7 PM IST.')

if __name__ == "__main__":
    main()
