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
        # Sidebar styling
        st.markdown(
            """
            <style>
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #ffffff 0%, #f9f9f9 50%, #f0f0f0 100%);
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .sidebar-title {
                text-align: center;
                font-size: 28px;
                color: #FF0000;
                font-weight: bold;
                margin-bottom: 0.5rem;
            }
            .trending-animation {
                text-align: center;
                font-size: 18px;
                margin-bottom: 1rem;
                animation: pulse 1.5s infinite;
                font-weight: 600;
                color: #FF0000;
            }
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }
           button[kind="secondary"] {
                width: 300px;  /* Keep the width same */
                padding: 0.8rem 1rem;  /* Keep the padding same */
                margin: 0.4rem 0;
                border-radius: 12px;  /* Keep rounded corners */
                color: #333;
                background-color: #fff;
                border: 3px solid #ddd;
                font-size: 16px;  
                font-weight: 600;
                text-transform: uppercase;  
                letter-spacing: 1px;  /* Add spacing between letters */
                transition: all 0.3s ease-in-out;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);  /* Soft shadow for a floating effect */
                cursor: pointer;  /* Indicate that the button is clickable */
            }

            button[kind="secondary"]:hover {
                background-color: #ffebeb;  
                color: #c40000;
                border-color: #ff0000;
                transform: translateY(-3px);  
                box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15);  
            }

            button.selected {
                background-color: #ff0000 !important;
                color: white !important;
                border: 2px solid #ff0000 !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);  
            }


            </style>
            """,
            unsafe_allow_html=True
        )

        # Logo & animation
        st.image("https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg", width=200)
        # st.markdown('<div class="sidebar-title">Trending Analysis</div>', unsafe_allow_html=True)
        # st.markdown('<div class="trending-animation">🔥 YouTube Trending 🔥</div>', unsafe_allow_html=True)
        st.markdown("---")

        # Session state
        if "selected_tab" not in st.session_state:
            st.session_state.selected_tab = "🏠 Home"

        # Buttons (styled using CSS above)
        if st.button("🏠 Home"):
            st.session_state.selected_tab = "🏠 Home"
        if st.button("🔍 Fetch and Analysis"):
            st.session_state.selected_tab = "🔍 Fetch and Analysis"
        if st.button("📊 Visuals"):
            st.session_state.selected_tab = "📊 Visuals"
        if st.button("ℹ️ About"):
            st.session_state.selected_tab = "ℹ️ About"


def home():
    st.title("🏠 Welcome to the Ultimate YouTube Data Analysis Experience 🚀")

    st.markdown("""
    ### 🎬 Dive Into YouTube Trends
    Explore **YouTube's trending videos** dataset to uncover patterns, such as:
    - 📈 What makes a video go viral?
    - 🕒 How timing and content types impact performance.
    - 🧠 Discover correlations between video metrics and engagement.

    ---  

    ### 🔍 Project Overview:
    - Fetch live trending data via **YouTube Data API v3**
    - Clean and preprocess data
    - Visualize insights: categories, views, engagement, etc.

    --- 

    ### 🚀 Skills You’ll Gain:
    | Skill Area           | Tools & Techniques         |
    |----------------------|----------------------------|
    | API Integration      | YouTube API v3, Python     |
    | Data Wrangling       | Pandas, Python             |
    | Visualization        | Matplotlib, Seaborn        |
    | Data Insights        | Statistical Analysis       |
    
    --- 

    ### 👨‍💻 Perfect For:
    - Aspiring Data Scientists
    - Portfolio Builders
    - YouTube Analysts & Creators

    > ✨ "Turn streams of video into streams of insight."  
    """, unsafe_allow_html=True)





def fetch_and_analysis():
    st.title("🔍 Fetch and Analyze Trending Videos")

    # Info icon for API Key guidance
    # with st.expander("❓ How to get your YouTube API Key", expanded=False):
    #     st.markdown("""
    #     1. Go to [Google Cloud Console](https://console.cloud.google.com/).
    #     2. Create or select a project.
    #     3. Enable **YouTube Data API v3** in the API Library.
    #     4. Go to **Credentials** and click **Create Credentials → API key**.
    #     5. Copy the key and paste it below.
    #     """)

    api_key = st.text_input("Enter your YouTube API Key", type="password", 
                            help="ℹ️ You can get an API Key from https://console.cloud.google.com/apis/credentials")

    country_options = ['All Countries', 'US', 'IN', 'GB', 'CA', 'DE', 'FR', 'JP', 'KR', 'BR', 'AU']
    countries = st.multiselect(
        "Select countries to fetch trending videos",
        options=country_options,
        default=None,
        help="Select one or more countries"
    )

    if st.button("Fetch and Analyze"):
        if not api_key:
            st.error("❗ Please enter your API Key.")
        elif not countries:
            st.error("❗ Please select at least one country.")
        else:
            selected_countries = country_options[1:] if "All Countries" in countries else countries

            with st.spinner("Fetching trending videos 🎥... Please wait..."):
                category_mapping = get_category_mapping(api_key)
                trending_videos = get_trending_videos(api_key, category_mapping, selected_countries)
                save_to_csv(trending_videos, 'trending_videos.csv')

                df = load_data('trending_videos.csv')
                check_missing_and_dtypes(df)
                df = preprocess_data(df)

                st.session_state.df = df
                st.session_state.data_loaded = True

            st.success("✅ Data fetched, cleaned, and ready!")

            # Show full dataframe for multiple or all countries
            if "All Countries" in countries or len(countries) > 1:
                st.dataframe(df)
            else:
                st.dataframe(df.head())

            # CSV download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name='trending_videos.csv',
                mime='text/csv'
            )




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