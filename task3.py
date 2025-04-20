#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import pytz
import streamlit as st

def main():
    apps = pd.read_csv('google playstore data.csv')

    apps = apps[apps['Installs'].str.contains(r'\d', regex=True, na=False)]
    apps['Installs'] = apps['Installs'].str.replace('[,+]', '', regex=True).astype(float)

    apps = apps[apps['Size'].str.contains(r'\d', regex=True, na=False)]
    apps['Size'] = apps['Size'].str.replace('M', '', regex=True)
    apps['Size'] = apps['Size'].str.replace('k', '', regex=True).astype(float) / 1025

    filter_df = apps[(apps['Rating'] >= 4.0) & (apps['Size'] >= 0.01)]
    filter_df['Last Updated'] = pd.to_datetime(filter_df['Last Updated'], errors='coerce')
    filter_df = filter_df[filter_df['Last Updated'].dt.month == 1]

    top10_cat = filter_df.groupby('Category').agg({
        'Rating': 'mean',
        'Reviews': 'count',
        'Installs': 'sum'
    }).nlargest(10, 'Installs').reset_index()

    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    current_hour = current_time.hour

    if 15 <= current_hour < 17:
        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='Average Rating',
            x=top10_cat['Category'],
            y=top10_cat['Rating'],
            yaxis='y1'
        ))

        fig.add_trace(go.Bar(
            name='Total Reviews',
            x=top10_cat['Category'],
            y=top10_cat['Reviews'],
            yaxis='y2'
        ))

        fig.update_layout(
            title='Average Rating and Total Reviews for Top 10 App Categories',
            xaxis=dict(title='App Categories'),
            yaxis=dict(title='Average Rating', side='left'),
            yaxis2=dict(
                title='Total Reviews',
                overlaying='y',
                side='right'
            ),
            barmode='group',
            height=600,
            width=1000
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        print("Graph can only be viewed between 3 PM and 5 PM IST.")

if __name__ == "__main__":
    main()
