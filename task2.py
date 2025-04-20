#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, time
import numpy as np
import regex as re
import streamlit as st

def clean_size(size):
    if isinstance(size, str):
        if 'M' in size:
            return float(size.replace('M', ''))
        elif 'k' in size:
            return float(size.replace('k', '')) / 1000
    return np.nan

def clean_android_ver(version):
    match = re.search(r'\d+(\.\d+)?', str(version))
    return float(match.group()) if match else np.nan

def main():
    df = pd.read_csv("google playstore data.csv")

    df = df[df["Installs"].str.contains(r'\d', regex=True, na=False)]
    df['Installs'] = df['Installs'].str.replace('[+,]', '', regex=True).astype(float)
    df['Price'] = df['Price'].str.replace('[$]', '', regex=True).astype(float)
    df['Size'] = df['Size'].apply(clean_size)
    df['Android Ver'] = df['Android Ver'].apply(clean_android_ver)
    df['Revenue'] = np.where(df['Type'] == 'Paid', df['Installs'] * df['Price'], 0)

    filtered_df = df[
        (df['Installs'] >= 10000) &
        (df['Revenue'] >= 10000) &
        (df['Android Ver'] > 4.0) &
        (df['Size'] > 15) &
        (df['Content Rating'] == 'Everyone') &
        (df['App'].str.len() <= 30)
    ]

    grouped = filtered_df.groupby(['Category', 'Type']).agg({
        'Installs': 'mean',
        'Revenue': 'mean'
    }).reset_index()

    top_3_cats = filtered_df['Category'].value_counts().head(3).index
    top_3_groups = grouped[grouped['Category'].isin(top_3_cats)]

    current_time = datetime.now().time()
    start_time = time(13, 0)
    end_time = time(14, 0)

    if start_time <= current_time <= end_time:
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=top_3_groups['Category'],
            y=top_3_groups['Installs'],
            name='Average Installs',
            marker_color='blue'
        ))

        fig.add_trace(go.Scatter(
            x=top_3_groups['Category'],
            y=top_3_groups['Revenue'],
            mode='lines+markers',
            name='Average Revenue',
            marker_color='red',
            yaxis='y2'
        ))

        fig.update_layout(
            title='Comparison of Average Installs and Revenue for Top 3 App Categories',
            xaxis_title='App Categories',
            yaxis=dict(title='Average Installs'),
            yaxis2=dict(
                title='Average Revenue ($)',
                overlaying='y',
                side='right'
            ),
            legend=dict(x=0.1, y=1.1),
            height=600,
            width=1000
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        print("The chart can only be viewed between 1 PM and 2 PM IST.")

if __name__ == "__main__":
    main()
