import pandas as pd

# Load the saved trending videos dataset
trending_videos = pd.read_csv('trending_videos.csv')

# Display the first few rows
print("📈 Top 5 Trending Videos in the US:\n")
print(trending_videos.head())
