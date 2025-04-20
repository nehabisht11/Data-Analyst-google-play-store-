#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import plotly.express as px
import datetime as dt
import pytz
import streamlit as st

def main():
    app = pd.read_csv('google playstore data.csv')

    app = app[app['Reviews'].str.contains(r'\d', regex=True, na=False)]
    app['Reviews'] = pd.to_numeric(app['Reviews'], errors='coerce').fillna(0).astype(int)

    app['Rating'] = app['Rating'].fillna(app['Rating'].mean())
    filter_app = app[
        (app['Rating'] < 4.0) &
        (app['Reviews'] > 10) &
        (app['App'].str.contains('C', case=False, na=False))
    ]

    category_count = filter_app['Category'].value_counts()
    valid_Category = category_count[category_count > 50].index
    filter_app = filter_app[filter_app['Category'].isin(valid_Category)]

    IST = pytz.timezone('Asia/Kolkata')
    current_time = dt.datetime.now(IST).time()
    start_time = dt.time(16, 0)
    end_time = dt.time(18, 0)

    if start_time <= current_time <= end_time:
        fig = px.violin(
            filter_app,
            x='Category',
            y='Rating',
            box=True,
            points="all",
            title="Distribution of Ratings for Each App Category",
            labels={"Category": "App Category", "Rating": "Rating"}
        )

        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        print("Graph is only visible between 4 PM - 6 PM IST.")

if __name__ == "__main__":
    main()
