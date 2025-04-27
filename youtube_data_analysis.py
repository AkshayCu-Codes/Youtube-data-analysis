import pandas as pd
from googleapiclient.discovery import build

# Replace with your actual API key
API_KEY = 'AIzaSyAwhwXmN6Uc5kS98o2xyWAUOTh1BbhUcjM'

# Fetch mapping from category ID to category name
def get_category_mapping(api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videoCategories().list(
        part='snippet',
        regionCode='US'
    )
    response = request.execute()
    category_mapping = {}
    for item in response['items']:
        category_id = int(item['id'])
        category_name = item['snippet']['title']
        category_mapping[category_id] = category_name
    return category_mapping

# Get trending videos with category names for multiple countries
def get_trending_videos(api_key, category_mapping, countries, max_results=200):
    youtube = build('youtube', 'v3', developerKey=api_key)
    all_videos = []

    for country in countries:
        request = youtube.videos().list(
            part='snippet,contentDetails,statistics',
            chart='mostPopular',
            regionCode=country,
            maxResults=50
        )

        while request and len(all_videos) < max_results:
            response = request.execute()
            for item in response['items']:
                video_details = {
                    'video_id': item['id'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'published_at': item['snippet']['publishedAt'],
                    'channel_id': item['snippet']['channelId'],
                    'channel_title': item['snippet']['channelTitle'],
                    'category_id': item['snippet']['categoryId'],
                    'category_name': category_mapping.get(int(item['snippet']['categoryId']), 'Unknown'),
                    'tags': item['snippet'].get('tags', []),
                    'duration': item['contentDetails']['duration'],
                    'definition': item['contentDetails']['definition'],
                    'caption': item['contentDetails'].get('caption', 'false'),
                    'view_count': item['statistics'].get('viewCount', 0),
                    'like_count': item['statistics'].get('likeCount', 0),
                    'dislike_count': item['statistics'].get('dislikeCount', 0),
                    'favorite_count': item['statistics'].get('favoriteCount', 0),
                    'comment_count': item['statistics'].get('commentCount', 0),
                    'country': country  # Adding the country information
                }
                all_videos.append(video_details)

            request = youtube.videos().list_next(request, response)

    return all_videos[:max_results]

# Save to CSV
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

# Main function
def main():
    category_mapping = get_category_mapping(API_KEY)
    
    # List of countries (you can add more country codes)
    countries = ['US', 'IN', 'GB', 'CA', 'DE']
    
    # US: United States
    # IN: India
    # GB: United Kingdom
    # CA: Canada
    # DE: Germany
    
    trending_videos = get_trending_videos(API_KEY, category_mapping, countries)
    filename = 'trending_videos_by_country.csv'
    save_to_csv(trending_videos, filename)
    print(f'Trending videos saved to {filename}')

if __name__ == '__main__':
    main()
