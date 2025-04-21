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

# Import visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")

# Distribution plots for views, likes, and comments
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# View Count Distribution
sns.histplot(trending_videos['view_count'], bins=30, kde=True, ax=axes[0], color='blue')
axes[0].set_title('View Count Distribution')
axes[0].set_xlabel('View Count')
axes[0].set_ylabel('Frequency')

# Like Count Distribution
sns.histplot(trending_videos['like_count'], bins=30, kde=True, ax=axes[1], color='green')
axes[1].set_title('Like Count Distribution')
axes[1].set_xlabel('Like Count')
axes[1].set_ylabel('Frequency')

# Comment Count Distribution
sns.histplot(trending_videos['comment_count'], bins=30, kde=True, ax=axes[2], color='red')
axes[2].set_title('Comment Count Distribution')
axes[2].set_xlabel('Comment Count')
axes[2].set_ylabel('Frequency')

# Show plots neatly
plt.tight_layout()
plt.savefig("distributions.png")
plt.show()
