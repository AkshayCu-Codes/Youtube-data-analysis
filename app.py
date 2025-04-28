# app.py
import streamlit as st
import pandas as pd
from youtube_data_analysis import get_category_mapping, get_trending_videos, save_to_csv
from data_exploration import load_data, check_missing_and_dtypes, preprocess_data, \
                               plot_distributions, plot_correlation_matrix, \
                               plot_boxplot_views, plot_category_distribution, \
                               plot_engagement_by_category, analyze_duration, \
                               analyze_tags, analyze_publish_hour

@st.cache_data
def fetch_data(api_key, countries):
    category_mapping = get_category_mapping(api_key)
    trending_videos = get_trending_videos(api_key, category_mapping, countries)
    save_to_csv(trending_videos, 'trending_videos.csv')
    return 'trending_videos.csv'

@st.cache_data
def prepare_data(csv_file):
    df = load_data(csv_file)
    check_missing_and_dtypes(df)
    df = preprocess_data(df)
    return df

def main():
    st.set_page_config(page_title="YouTube Trending Analysis", page_icon="📈", layout="wide")
    st.title("📈 YouTube Trending Video Analysis")

    # Initialize session state variables
    if "selected_tab" not in st.session_state:
        st.session_state.selected_tab = "🏠 Home"
    if "api_key" not in st.session_state:
        st.session_state.api_key = None
    if "countries" not in st.session_state:
        st.session_state.countries = None

    # Sidebar Tabs
    with st.sidebar:
        st.header("Navigation")
        selected_tab = st.selectbox(
            "Select a section",
            ["🏠 Home", "🔍 Fetch and Analysis", "📊 Visuals", "ℹ️ About"],
            index=["🏠 Home", "🔍 Fetch and Analysis", "📊 Visuals", "ℹ️ About"].index(st.session_state.selected_tab)
        )
        st.session_state.selected_tab = selected_tab
        st.markdown("---")

    if st.session_state.selected_tab == "🏠 Home":
        st.subheader("Welcome to YouTube Trending Video Analysis App!")
        st.write("""
            🔥 **Features**:
            - Fetch trending videos from YouTube
            - Preprocess and explore the dataset
            - Visualize important trends like views, likes, categories
            - Analyze best time to upload videos!
            
            ---
            👉 Switch tabs from the sidebar to Fetch and Explore data.
        """)

    elif st.session_state.selected_tab == "🔍 Fetch and Analysis":
        st.subheader("Fetch and Preprocess Trending Videos")

        api_key = st.text_input("🔑 Enter YouTube API Key", type="password")
        countries = st.multiselect(
            "🌎 Select countries",
            options=['US', 'IN', 'GB', 'CA', 'DE', 'FR', 'JP', 'KR', 'BR', 'AU'],
            default=[]
        )

        if st.button("🚀 Fetch and Analyze"):
            if not api_key:
                st.error("❗ Please enter your API Key.")
            elif not countries:
                st.error("❗ Please select at least one country.")
            else:
                with st.spinner("Fetching trending videos..."):
                    csv_file = fetch_data(api_key, countries)
                st.success("✅ Trending videos fetched and saved!")

                with st.spinner("Loading and preprocessing data..."):
                    df = prepare_data(csv_file)
                st.success("✅ Data loaded and preprocessed!")

                # Save API Key and countries to session
                st.session_state.api_key = api_key
                st.session_state.countries = countries

                # Automatically move to Visuals tab
                st.session_state.selected_tab = "📊 Visuals"
                st.experimental_rerun()  # Important: This forces rerun immediately

    elif st.session_state.selected_tab == "📊 Visuals":
        st.subheader("📊 Data Visualizations")

        # Use session state values
        api_key = st.session_state.api_key
        countries = st.session_state.countries

        if not api_key or not countries:
            st.error("⚠️ Please first Fetch data from 'Fetch and Analysis' tab.")
        else:
            try:
                df = prepare_data('trending_videos.csv')

                with st.expander("📈 View, Like, Comment Distribution", expanded=False):
                    plot_distributions(df)
                    st.pyplot()

                with st.expander("📈 Correlation Matrix of Engagement Metrics", expanded=False):
                    plot_correlation_matrix(df)
                    st.pyplot()

                with st.expander("📈 Boxplot of View Counts", expanded=False):
                    plot_boxplot_views(df)
                    st.pyplot()

                with st.expander("📈 Distribution of Trending Videos by Category", expanded=False):
                    plot_category_distribution(df)
                    st.pyplot()

                with st.expander("📈 Average Engagement Metrics by Category", expanded=False):
                    plot_engagement_by_category(df)
                    st.pyplot()

                with st.expander("📈 Duration vs View Count", expanded=False):
                    analyze_duration(df)
                    st.pyplot()

                with st.expander("📈 Tags vs View Count", expanded=False):
                    analyze_tags(df)
                    st.pyplot()

                with st.expander("📈 Publish Hour vs View Count", expanded=False):
                    analyze_publish_hour(df)
                    st.pyplot()

            except Exception as e:
                st.error(f"⚠️ Error loading data: {e}")

    elif st.session_state.selected_tab == "ℹ️ About":
        st.subheader("About This App")
        st.write("""
            - **Developer**: Akshay CU 🚀
            - **Purpose**: Analyze YouTube Trending Videos
            - **Tech Stack**: Streamlit, YouTube Data API v3, Pandas, Matplotlib
            - **GitHub Repository**: [link your repo here]
            - **Contact**: [link your LinkedIn/Email]
            
            ---
            Built with ❤️ using Streamlit
        """)

if __name__ == "__main__":
    main()
