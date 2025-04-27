import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import isodate

sns.set(style="whitegrid")

def load_data(filepath):
    df = pd.read_csv(filepath)
    return df

def check_missing_and_dtypes(df):
    print("Missing Values:\n", df.isnull().sum())
    print("\nData Types:\n", df.dtypes)

def preprocess_data(df):
    df['description'].fillna('No description', inplace=True)
    df['published_at'] = pd.to_datetime(df['published_at'])
    df['tags'] = df['tags'].apply(lambda x: eval(x) if isinstance(x, str) else x)
    return df

def plot_distributions(df):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    sns.histplot(df['view_count'], bins=30, kde=True, ax=axes[0], color='blue')
    sns.histplot(df['like_count'], bins=30, kde=True, ax=axes[1], color='green')
    sns.histplot(df['comment_count'], bins=30, kde=True, ax=axes[2], color='red')

    axes[0].set_title('View Count Distribution')
    axes[1].set_title('Like Count Distribution')
    axes[2].set_title('Comment Count Distribution')
    plt.tight_layout()
    plt.savefig("distributions.png")
    plt.show()

def plot_correlation_matrix(df):
    correlation_matrix = df[['view_count', 'like_count', 'comment_count']].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, linecolor='black')
    plt.title('Correlation Matrix of Engagement Metrics')
    plt.show()

def plot_boxplot_views(df):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df['view_count'], color='purple')
    plt.title('Boxplot of View Counts')
    plt.xlabel('View Count')
    plt.show()

def plot_category_distribution(df):
    plt.figure(figsize=(12, 8))
    sns.countplot(
        y=df['category_name'],
        order=df['category_name'].value_counts().index,
        palette='viridis'
    )
    plt.title('Number of Trending Videos by Category')
    plt.xlabel('Number of Videos')
    plt.ylabel('Category')
    plt.tight_layout()
    plt.savefig("category_distribution.png")
    plt.show()

def plot_engagement_by_category(df):
    category_engagement = df.groupby('category_name')[['view_count', 'like_count', 'comment_count']]\
                            .mean().sort_values(by='view_count', ascending=False)
    fig, axes = plt.subplots(1, 3, figsize=(18, 10))
    sns.barplot(y=category_engagement.index, x=category_engagement['view_count'], ax=axes[0], palette='viridis')
    sns.barplot(y=category_engagement.index, x=category_engagement['like_count'], ax=axes[1], palette='viridis')
    sns.barplot(y=category_engagement.index, x=category_engagement['comment_count'], ax=axes[2], palette='viridis')

    axes[0].set_title('Average View Count by Category')
    axes[1].set_title('Average Like Count by Category')
    axes[2].set_title('Average Comment Count by Category')

    plt.tight_layout()
    plt.savefig("average_engagement_by_category.png")
    plt.show()

def analyze_duration(df):
    df['duration_seconds'] = df['duration'].apply(lambda x: isodate.parse_duration(x).total_seconds())
    df['duration_range'] = pd.cut(df['duration_seconds'], bins=[0, 300, 600, 1200, 3600, 7200],
                                  labels=['0-5 min', '5-10 min', '10-20 min', '20-60 min', '60-120 min'])

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='duration_seconds', y='view_count', data=df, alpha=0.6, color='purple')
    plt.title('Video Length vs View Count')
    plt.xlabel('Video Length (seconds)')
    plt.ylabel('View Count')
    plt.show()

    length_engagement = df.groupby('duration_range')[['view_count', 'like_count', 'comment_count']].mean()
    fig, axes = plt.subplots(1, 3, figsize=(18, 8))

    sns.barplot(y=length_engagement.index, x=length_engagement['view_count'], ax=axes[0], palette='magma')
    sns.barplot(y=length_engagement.index, x=length_engagement['like_count'], ax=axes[1], palette='magma')
    sns.barplot(y=length_engagement.index, x=length_engagement['comment_count'], ax=axes[2], palette='magma')

    axes[0].set_title('Average View Count by Duration Range')
    axes[1].set_title('Average Like Count by Duration Range')
    axes[2].set_title('Average Comment Count by Duration Range')

    plt.tight_layout()
    plt.show()

def analyze_tags(df):
    df['tag_count'] = df['tags'].apply(len)

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='tag_count', y='view_count', data=df, alpha=0.6, color='orange')
    plt.title('Number of Tags vs View Count')
    plt.xlabel('Number of Tags')
    plt.ylabel('View Count')
    plt.show()

def analyze_publish_hour(df):
    df['publish_hour'] = df['published_at'].dt.hour

    plt.figure(figsize=(12, 6))
    sns.countplot(x='publish_hour', data=df, palette='coolwarm')
    plt.title('Distribution of Videos by Publish Hour')
    plt.xlabel('Publish Hour')
    plt.ylabel('Number of Videos')
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='publish_hour', y='view_count', data=df, alpha=0.6, color='teal')
    plt.title('Publish Hour vs View Count')
    plt.xlabel('Publish Hour')
    plt.ylabel('View Count')
    plt.show()

def main():
    filepath = 'trending_videos.csv'
    df = load_data(filepath)
    
    check_missing_and_dtypes(df)
    
    df = preprocess_data(df)
    
    df[['view_count', 'like_count', 'dislike_count', 'comment_count']].describe().to_csv('descriptive_stats.csv')
    
    plot_distributions(df)
    plot_correlation_matrix(df)
    plot_boxplot_views(df)
    plot_category_distribution(df)
    plot_engagement_by_category(df)
    analyze_duration(df)
    analyze_tags(df)
    analyze_publish_hour(df)

if __name__ == "__main__":
    main()
