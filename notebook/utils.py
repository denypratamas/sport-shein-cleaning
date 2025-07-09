import pandas as pd
import numpy as np

def convert_sold_to_int(s):
    """
    Convert selling proposition string (e.g., '1.2k sold recently') to integer.
    """
    if pd.isna(s):
        return np.nan
    s = str(s).lower().replace('sold recently', '').replace('+', '').strip()
    if 'k' in s:
        return int(float(s.replace('k', '').strip()) * 1000)
    else:
        return int(s.strip())


def process_rank_column(df):
    """
    Split 'rank-title' and clean 'rank-sub' into rank_number, rank_type, rank_category.
    """
    def split_rank_title(s):
        if pd.isna(s):
            return pd.Series([np.nan, np.nan])
        parts = str(s).strip().split(' ', 1)
        try:
            rank_number = int(parts[0].replace('#', '').strip())
            rank_type = parts[1].strip()
            return pd.Series([rank_number, rank_type])
        except:
            return pd.Series([np.nan, np.nan])

    def clean_rank_category(s):
        if pd.isna(s):
            return np.nan
        return str(s).replace('in ', '', 1).strip()

    df[['rank_number', 'rank_type']] = df['rank-title'].apply(split_rank_title)
    df['rank_category'] = df['rank-sub'].apply(clean_rank_category)
    df['is_ranked'] = df['rank_number'].notna().astype(int)
    df.drop(['rank-title', 'rank-sub'], axis=1, inplace=True)

    return df


def merge_columns(df, new_col_name, primary_col, secondary_col):
    """
    Merge two columns into one, prioritizing non-null values from primary_col.
    """
    df[new_col_name] = df[primary_col].fillna(df[secondary_col])
    df.drop([primary_col, secondary_col], axis=1, inplace=True)
    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Master function to clean Shein dataset.
    - Drops useless columns
    - Cleans prices and discounts
    - Converts sales text to int
    - Merges inconsistent product title columns
    - Parses rank info into structured columns
    """
    df = df.copy()

    # Drop unnecessary/noisy columns
    cols_to_drop = [
        'goods-title-link--jump href',
        'color-count',
        'blackfridaybelts-bg src',
        'blackfridaybelts-content'
    ]
    df.drop(columns=cols_to_drop, inplace=True, errors='ignore')

    # Merge inconsistent title columns (optional based on your dataset)
    if 'goods-title-link--jump' in df.columns and 'goods-title-link' in df.columns:
        df = merge_columns(df, 'product_title', 'goods-title-link--jump', 'goods-title-link')

    # Clean price
    if 'price' in df.columns:
        df['price'] = df['price'].astype(str).str.replace('$', '', regex=False).str.replace(',', '.', regex=False)
        df['price'] = pd.to_numeric(df['price'], errors='coerce')

    # Clean discount
    if 'discount' in df.columns:
        df['discount'] = df['discount'].fillna('0%').str.replace('%', '', regex=False)
        df['discount'] = pd.to_numeric(df['discount'], errors='coerce').abs()

    # Clean selling proposition
    if 'selling_proposition' in df.columns:
        df['selling_proposition'] = df['selling_proposition'].apply(convert_sold_to_int)
        df['selling_proposition'] = df['selling_proposition'].fillna(0).astype(int)

    # Parse rank-related columns
    if 'rank-title' in df.columns and 'rank-sub' in df.columns:
        df = process_rank_column(df)

    return df
