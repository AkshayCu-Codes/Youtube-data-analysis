# app.py
import streamlit as st
import pandas as pd
from youtube_data_analysis import get_category_mapping, get_trending_videos, save_to_csv
from data_exploration import load_data, check_missing_and_dtypes, preprocess_data, \
                               plot_distributions, plot_correlation_matrix, \
                               plot_boxplot_views, plot_category_distribution, \
                               plot_engagement_by_category, analyze_duration, \
                               analyze_tags, analyze_publish_hour

# Cache API fetching
@st.cache_data
def fetch_data(api_key, countries):
    category_mapping = get_category_mapping(api_key)
    trending_videos = get_trending_videos(api_key, category_mapping, countries)
    save_to_csv(trending_videos, 'trending_videos.csv')
    return 'trending_videos.csv'

# Cache loading and preprocessing
@st.cache_data
def prepare_data(csv_file):
    df = load_data(csv_file)
    check_missing_and_dtypes(df)
    df = preprocess_data(df)
    return df

def main():
    st.set_page_config(page_title="YouTube Trending Analysis", page_icon="📈", layout="wide")
    st.title("📈 YouTube Trending Video Analysis")

    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("Enter your YouTube API Key", type="password")
        countries = st.multiselect(
            "Select countries to fetch trending videos",
            options=['US', 'IN', 'GB', 'CA', 'DE', 'FR', 'JP', 'KR', 'BR', 'AU'],
            default=['US']
        )
        section = st.radio("Go to Section:", [
            "Home", "Fetch and Analyze", "Data Visualizations"
        ])

    if section == "Home":
        st.subheader("Welcome to the YouTube Trending Video Analysis App!")
        st.write("""
            📹 This app lets you:
            - Fetch trending videos from YouTube API
            - Preprocess and explore the data
            - Visualize important metrics and trends
            ---
            Go to the **Sidebar** to fetch and analyze trending videos!
        """)

    elif section == "Fetch and Analyze":
        st.subheader("Fetch Trending Videos")
        if st.button("Fetch and Analyze Data"):
            if not api_key:
                st.error("❗ Please enter your API Key.")
            elif not countries:
                st.error("❗ Please select at least one country.")
            else:
                with st.spinner("Fetching trending videos..."):
                    csv_file = fetch_data(api_key, countries)
                st.success("✅ Data fetched and saved!")

                with st.spinner("Loading and preprocessing data..."):
                    df = prepare_data(csv_file)
                st.success("✅ Data loaded and preprocessed!")

                st.write(df.head())

    elif section == "Data Visualizations":
        st.subheader("📊 Data Visualizations")
        try:
            df = prepare_data('trending_videos.csv')

            with st.expander("View, Like, Comment Distribution"):
                plot_distributions(df)
                st.pyplot()

            with st.expander("Correlation Matrix of Engagement Metrics"):
                plot_correlation_matrix(df)
                st.pyplot()

            with st.expander("Boxplot of View Counts"):
                plot_boxplot_views(df)
                st.pyplot()

            with st.expander("Distribution of Trending Videos by Category"):
                plot_category_distribution(df)
                st.pyplot()

            with st.expander("Average Engagement Metrics by Category"):
                plot_engagement_by_category(df)
                st.pyplot()

            with st.expander("Duration vs View Count"):
                analyze_duration(df)
                st.pyplot()

            with st.expander("Tags vs View Count"):
                analyze_tags(df)
                st.pyplot()

            with st.expander("Publish Hour vs View Count"):
                analyze_publish_hour(df)
                st.pyplot()

        except Exception as e:
            st.error(f"⚠️ Error loading data: {e}")
            st.info("Please fetch and preprocess data first from the 'Fetch and Analyze' section.")

if __name__ == "__main__":
    main()
