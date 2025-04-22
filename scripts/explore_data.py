import pandas as pd

def load_data(filepath):
    df = pd.read_csv(filepath)
    df['description'].fillna('No description', inplace=True)
    df['published_at'] = pd.to_datetime(df['published_at'])
    df['tags'] = df['tags'].apply(lambda x: eval(x) if isinstance(x, str) else x)
    return df

def get_descriptive_stats(df):
    return df[['view_count', 'like_count', 'dislike_count', 'comment_count']].describe()
