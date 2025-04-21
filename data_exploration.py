import pandas as pd

# Load the saved data
trending_videos = pd.read_csv('trending_videos.csv')

# Check for missing values
missing_values = trending_videos.isnull().sum()

# Display data types
data_types = trending_videos.dtypes

print("Missing Values:\n", missing_values)
print("\nData Types:\n", data_types)
