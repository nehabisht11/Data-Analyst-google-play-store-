#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import datetime as dt
import plotly.express as px
import pytz
import streamlit as st

def main():
    app = pd.read_csv('googleplaystore_with_countries.csv')

    app = app[app['Installs'].str.contains(r'\d', regex=True, na=False)]
    app['Installs'] = app['Installs'].str.replace('[,+]', '', regex=True).astype(int)

    filter_app = app[~app['Category'].str.contains(r'(?i)^[ACGS]', regex=True)]
    filter_app = filter_app[filter_app['Installs'] > 1_000_000]

    group = filter_app.groupby(['Category', 'Countries']).agg({'Installs': 'sum'}).reset_index()
    top_5_cat = group.groupby('Category')['Installs'].sum().nlargest(5).index
    top_data = group[group['Category'].isin(top_5_cat)]

    IST = pytz.timezone('Asia/Kolkata')
    current_time = dt.datetime.now(IST).time()
    start_time = dt.time(18, 0)
    end_time = dt.time(20, 0)

    if start_time <= current_time <= end_time:
        fig = px.choropleth(
            top_data,
            locations="Countries",
            locationmode="country names",
            color="Installs",
            hover_name="Category",
            animation_frame="Category",
            color_continuous_scale="YlOrRd",
            title="Global App Installs (Filtered Top 5 Categories)"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        print("Choropleth map visible only between 6 PM to 8 PM IST.")

if __name__ == "__main__":
    main()
