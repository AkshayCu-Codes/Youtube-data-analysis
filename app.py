# app.py
import streamlit as st
import pandas as pd
from youtube_data_analysis import get_category_mapping, get_trending_videos, save_to_csv
from data_exploration import load_data, check_missing_and_dtypes, preprocess_data, \
                               plot_distributions, plot_correlation_matrix, \
                               plot_boxplot_views, plot_category_distribution, \
                               plot_engagement_by_category, analyze_duration, \
                               analyze_tags, analyze_publish_hour


def main():
    st.title("📈 YouTube Trending Video Analysis")

    st.sidebar.header("Configuration")
    api_key = st.sidebar.text_input("Enter your YouTube API Key", type="password")
    
    countries = st.sidebar.multiselect(
        "Select countries to fetch trending videos",
        options=['US', 'IN', 'GB', 'CA', 'DE', 'FR', 'JP', 'KR', 'BR', 'AU'],
        default=['US']
    )

    if st.sidebar.button("Fetch and Analyze"):
        if not api_key:
            st.error("❗ Please enter your API Key.")
        elif not countries:
            st.error("❗ Please select at least one country.")
        else:
            st.success("Fetching trending videos... Please wait.")
            
            # Fetch data
            category_mapping = get_category_mapping(api_key)
            trending_videos = get_trending_videos(api_key, category_mapping, countries)
            save_to_csv(trending_videos, 'trending_videos.csv')

            # Load and preprocess
            df = load_data('trending_videos.csv')
            check_missing_and_dtypes(df)
            df = preprocess_data(df)

            st.success("✅ Data loaded and preprocessed!")
            st.write(df.head())

            # Plots
            st.header("📊 Data Visualizations")
            
            # Show Distribution Plots
            st.subheader("View, Like, Comment Distribution")
            plot_distributions(df)
            st.pyplot()  # To display the plot in Streamlit

            # Show Correlation Matrix
            st.subheader("Correlation Matrix of Engagement Metrics")
            plot_correlation_matrix(df)
            st.pyplot()

            # Show Boxplot Views
            st.subheader("Boxplot of View Counts")
            plot_boxplot_views(df)
            st.pyplot()

            # Show Category Distribution
            st.subheader("Distribution of Trending Videos by Category")
            plot_category_distribution(df)
            st.pyplot()

            # Show Average Engagement by Category
            st.subheader("Average Engagement Metrics by Category")
            plot_engagement_by_category(df)
            st.pyplot()

            # Duration Analysis
            st.subheader("Duration vs View Count")
            analyze_duration(df)
            st.pyplot()

            # Tag Analysis
            st.subheader("Tags vs View Count")
            analyze_tags(df)
            st.pyplot()

            # Publish Hour Analysis
            st.subheader("Publish Hour vs View Count")
            analyze_publish_hour(df)
            st.pyplot()


if __name__ == "__main__":
    main()
