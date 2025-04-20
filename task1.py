#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
import nltk
import plotly.express as px
import numpy as np
import streamlit as st

def main():
    nltk.download('stopwords')

    # Load datasets
    apps_df = pd.read_csv('google playstore data.csv')
    review_df = pd.read_csv('user reviews data.csv')

    # Filter for Health & Fitness apps
    health_fitness_apps = apps_df[apps_df['Category'] == 'HEALTH_AND_FITNESS']['App'].unique()

    # Filter reviews for Health & Fitness apps
    health_fitness_reviews = review_df[review_df['App'].isin(health_fitness_apps)]

    # Filter positive (5-star) reviews
    positive_reviews = health_fitness_reviews[health_fitness_reviews['Sentiment'] == 'Positive']
    positive_reviews = positive_reviews.dropna(subset=['Translated_Review'])

    # Combine all review texts
    all_text = ' '.join(positive_reviews['Translated_Review'])

    # Remove stopwords and app names
    custom_stopwords = set(stopwords.words('english'))
    custom_stopwords.update(map(str.lower, health_fitness_apps))

    # Generate word cloud
    wordcloud = WordCloud(
        width=700,
        height=300,
        stopwords=custom_stopwords,
        background_color='#2B1E40'
    ).generate(all_text)

    # Convert wordcloud to array
    img_array = wordcloud.to_array()

    # Use plotly to show image
    fig = px.imshow(img_array)
    fig.update_layout(
        title='Word Cloud for Most Frequent Keywords in 5-Star Health & Fitness App Reviews',
        xaxis_visible=False,
        yaxis_visible=False,
        plot_bgcolor='white'
    )
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
