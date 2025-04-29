# app.py
import streamlit as st
import pandas as pd
from youtube_data_analysis import get_category_mapping, get_trending_videos, save_to_csv
from data_exploration import load_data, check_missing_and_dtypes, preprocess_data, \
                               plot_distributions, plot_correlation_matrix, \
                               plot_boxplot_views, plot_category_distribution, \
                               plot_engagement_by_category, analyze_duration, \
                               analyze_tags, analyze_publish_hour

# Initialize session state
if "selected_tab" not in st.session_state:
    st.session_state.selected_tab = "🏠 Home"
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

def sidebar():
    with st.sidebar:
        # Background styling
        st.markdown(
            """
            <style>
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #ffffff 0%, #f9f9f9 50%, #f0f0f0 100%);
            }
            .sidebar-title {
                text-align: center;
                font-size: 28px;
                color: #FF0000;
                font-weight: bold;
            }
            .nav-button {
                display: block;
                width: 100%;
                text-align: left;
                padding: 0.75rem 1rem;
                margin: 0.3rem 0;
                border-radius: 8px;
                color: black;
                background-color: #ffffff;
                border: 1px solid #ddd;
                font-size: 16px;
                font-weight: 500;
                transition: background-color 0.3s ease;
            }
            .nav-button:hover {
                background-color: #ffeaea;
                color: #c40000;
                border-color: #ff0000;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # YouTube logo centered
        st.image("https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg", width=200)

        st.markdown('<div class="sidebar-title">Trending Analysis</div>', unsafe_allow_html=True)
        st.markdown("---")

        # Navigation buttons
        if st.button("🏠 Home", key="home_btn"):
            st.session_state.selected_tab = "🏠 Home"
        if st.button("🔍 Fetch and Analysis", key="fetch_btn"):
            st.session_state.selected_tab = "🔍 Fetch and Analysis"
        if st.button("📊 Visuals", key="visuals_btn"):
            st.session_state.selected_tab = "📊 Visuals"
        if st.button("ℹ️ About", key="about_btn"):
            st.session_state.selected_tab = "ℹ️ About"

        st.markdown("---")
        st.subheader("📚 About")
        st.caption("🔴 Explore YouTube's Trending Videos and understand viral patterns!")
        st.caption("Developed by Akshay CU 🚀")

        st.markdown("---")
        st.caption("Made with ❤️ using Streamlit.")


def home():
    st.title("🏠 Home")
    st.markdown("Welcome to **YouTube Trending Video Analysis**! 🎬 \n\nExplore YouTube's trending videos, analyze patterns, and gain insights!")

def fetch_and_analysis():
    st.title("🔍 Fetch and Analyze Trending Videos")
    
    api_key = st.text_input("Enter your YouTube API Key", type="password")
    
    countries = st.multiselect(
        "Select countries to fetch trending videos",
        options=['US', 'IN', 'GB', 'CA', 'DE', 'FR', 'JP', 'KR', 'BR', 'AU'],
        help="Select one or more countries"
    )

    if st.button("Fetch and Analyze"):
        if not api_key:
            st.error("❗ Please enter your API Key.")
        elif not countries:
            st.error("❗ Please select at least one country.")
        else:
            with st.spinner("Fetching trending videos 🎥... Please wait..."):
                category_mapping = get_category_mapping(api_key)
                trending_videos = get_trending_videos(api_key, category_mapping, countries)
                save_to_csv(trending_videos, 'trending_videos.csv')

                df = load_data('trending_videos.csv')
                check_missing_and_dtypes(df)
                df = preprocess_data(df)
                
                st.session_state.df = df
                st.session_state.data_loaded = True

            st.success("✅ Data fetched, cleaned and ready!")
            st.dataframe(df.head())

def visuals():
    st.title("📊 Visualizations")

    if not st.session_state.get("data_loaded", False):
        st.warning("⚠️ Please fetch data first from the 'Fetch and Analysis' tab!")
        return

    df = st.session_state.df

    st.header("📈 Data Visualizations")

    # Distribution Plots
    st.subheader("View, Like, Comment Distribution")
    plot_distributions(df)
    st.pyplot()

    # Correlation Matrix
    st.subheader("Correlation Matrix of Engagement Metrics")
    plot_correlation_matrix(df)
    st.pyplot()

    # Boxplot Views
    st.subheader("Boxplot of View Counts")
    plot_boxplot_views(df)
    st.pyplot()

    # Category Distribution
    st.subheader("Distribution of Trending Videos by Category")
    plot_category_distribution(df)
    st.pyplot()

    # Average Engagement by Category
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

def about():
    st.title("ℹ️ About This App")
    st.markdown("""
    This Streamlit app analyzes **YouTube trending videos** to uncover interesting patterns,
    like:
    - When videos are posted
    - How engagement (likes, comments) varies
    - Differences across countries and categories

    Developed with ❤️ by **Akshay CU**.
    """)

def main():
    st.set_page_config(page_title="YouTube Trending Analysis", page_icon="🎬", layout="wide")
    
    sidebar()

    tab = st.session_state.selected_tab

    if tab == "🏠 Home":
        home()
    elif tab == "🔍 Fetch and Analysis":
        fetch_and_analysis()
    elif tab == "📊 Visuals":
        visuals()
    elif tab == "ℹ️ About":
        about()

if __name__ == "__main__":
    main()
