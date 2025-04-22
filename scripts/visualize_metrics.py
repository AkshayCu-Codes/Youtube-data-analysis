import matplotlib.pyplot as plt
import seaborn as sns

def plot_distributions(df):
    sns.set(style="whitegrid")
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    sns.histplot(df['view_count'], bins=30, kde=True, ax=axes[0], color='blue')
    axes[0].set_title('View Count Distribution')
    axes[0].set_xlabel('View Count')
    axes[0].set_ylabel('Frequency')

    sns.histplot(df['like_count'], bins=30, kde=True, ax=axes[1], color='green')
    axes[1].set_title('Like Count Distribution')
    axes[1].set_xlabel('Like Count')
    axes[1].set_ylabel('Frequency')

    sns.histplot(df['comment_count'], bins=30, kde=True, ax=axes[2], color='red')
    axes[2].set_title('Comment Count Distribution')
    axes[2].set_xlabel('Comment Count')
    axes[2].set_ylabel('Frequency')

    plt.tight_layout()
    plt.show()

def plot_correlation_heatmap(df):
    correlation_matrix = df[['view_count', 'like_count', 'comment_count']].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, linecolor='black')
    plt.title('Correlation Matrix of Engagement Metrics')
    plt.show()
