#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import datetime as dt
import pytz
import plotly.express as px
import streamlit as st

def main():
    apps = pd.read_csv('google playstore data.csv')

    apps = apps[apps['Installs'].str.contains(r'\d', regex=True, na=False)]
    apps['Installs'] = apps['Installs'].str.replace('[,+]', '', regex=True).astype(int)

    filter_apps = apps[
        (apps['App'].str.startswith('E')) &
        (apps['Installs'] > 10000) &
        (apps['Content Rating'] == 'Teen')
    ]

    filter_apps['Last Updated'] = pd.to_datetime(filter_apps['Last Updated'], errors='coerce')
    filter_apps = filter_apps.dropna(subset=['Last Updated'])
    filter_apps['month_year'] = filter_apps['Last Updated'].dt.to_period('M')

    month_install = filter_apps.groupby(['Category', 'month_year']).agg({
        'Installs': 'sum'
    }).reset_index()

    month_install = month_install.sort_values(by=['Category', 'month_year'])
    month_install['previous'] = month_install.groupby('Category')['Installs'].shift(1)
    month_install['MoM'] = ((month_install['Installs'] - month_install['previous']) / month_install['previous']) * 100
    month_install['Significant'] = month_install['MoM'] > 20

    IST = pytz.timezone('Asia/Kolkata')
    current_time = dt.datetime.now(IST).time()
    start_time = dt.time(18, 0)
    end_time = dt.time(21, 0)

    if start_time <= current_time <= end_time:
        month_install['month_year'] = month_install['month_year'].astype(str)

        fig = px.line(
            month_install,
            x='month_year',
            y='Installs',
            color='Category',
            markers=True,
            title='Total Installs Trend Over Time (Segmented by App Category)'
        )

        highlight = month_install[month_install['Significant']]
        fig.add_scatter(
            x=highlight['month_year'],
            y=highlight['Installs'],
            mode='markers',
            marker=dict(size=8, color='red'),
            name='>20% MoM Growth'
        )

        fig.update_layout(
            xaxis_title='Month-Year',
            yaxis_title='Total Installs',
            xaxis_tickangle=-45,
            template='plotly_dark'
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        print('The graph is only available between 6 PM - 9 PM IST.')

if __name__ == "__main__":
    main()
