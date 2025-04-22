from scripts.fetch_trending import get_trending_videos, save_to_csv
from scripts.explore_data import load_data, get_descriptive_stats
from scripts.visualize_metrics import plot_distributions, plot_correlation_heatmap

API_KEY = 'Your API Key'
DATA_PATH = 'data/trending_videos.csv'

def main():
    # Fetch and save data
    videos = get_trending_videos(API_KEY)
    save_to_csv(videos, DATA_PATH)

    # Load and explore data
    df = load_data(DATA_PATH)
    print(get_descriptive_stats(df))

    # Visualize data
    plot_distributions(df)
    plot_correlation_heatmap(df)

if __name__ == '__main__':
    main()
