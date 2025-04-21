import pandas as pd

# Load the saved data
trending_videos = pd.read_csv('trending_videos.csv')

# Check for missing values
missing_values = trending_videos.isnull().sum()

# Display data types
data_types = trending_videos.dtypes

print("Missing Values:\n", missing_values)
print("\nData Types:\n", data_types)

# Fill missing descriptions with "No description"
trending_videos['description'].fillna('No description', inplace=True)

# Convert `published_at` to datetime
trending_videos['published_at'] = pd.to_datetime(trending_videos['published_at'])

# Convert tags from string representation of list to actual list
trending_videos['tags'] = trending_videos['tags'].apply(lambda x: eval(x) if isinstance(x, str) else x) 

print("Missing descriptions filled, published_at converted to datetime, and tags parsed to lists.")

# Descriptive statistics for key engagement metrics
descriptive_stats = trending_videos[['view_count', 'like_count', 'dislike_count', 'comment_count']].describe()

print("Descriptive statistics for engagement metrics:")
print(descriptive_stats)

descriptive_stats.to_csv('descriptive_stats.csv')
print("Descriptive statistics saved to descriptive_stats.csv")