import pandas as pd
import glob
import zipfile
import os
import sys

def merge_zip_file(folder_name):
    zip_files_name = os.path.join('../data/raw/itineraries_csv/', folder_name, f"{folder_name}_itineraries_*.zip")
    
    zip_files = glob.glob(zip_files_name)
    df_list = []
    
    for zip_file in zip_files:
        with zipfile.ZipFile(zip_file, 'r') as z:
            with z.open(z.namelist()[0]) as f:
                df = pd.read_csv(f)
                df_list.append(df)
    merge_df = pd.concat(df_list, ignore_index=True)
    return merge_df

def check_missing_value(df):
    missing_vals = df.isna().sum()
    missing_pct = (missing_vals / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'Column': missing_vals.index,
        'Missing Values': missing_vals.values,
        'Missing Percentage': missing_pct.values
    })
    
    missing_df = missing_df[missing_df['Missing Values'] > 0]
    missing_df = missing_df.sort_values(by='Missing Percentage', ascending=False)
    
    print("Column with missing values:")
    print(missing_df)
    return list(missing_df['Column'])

def plot_bar(df, x, y):
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x=x, y=y, palette='ch:.25')
    plt.xticks(rotation=90, ha='right')
    plt.title(f'Counts by {x}')
    
    plt.show()
    
def convert_to_unix_timestamp(df, col_name, date_format='%Y-%m-%d'):
    from datetime import datetime

    df[col_name] = df[col_name].apply(lambda x: datetime.timestamp(datetime.strptime(str(x), date_format)))
    
    return df

def duration_to_minutes(duration_str):
    import re
    
    match = re.match(r'PT(\d+H)?(\d+M)?', duration_str)
    if match:
        hours = int(match.group(1)[:-1]) if match.group(1) else 0
        minutes = int(match.group(2)[:-1]) if match.group(2) else 0
        return hours * 60 + minutes
    else:
        return None


def duration_to_hours(duration_str):
    total_minutes = duration_to_minutes(duration_str)
    return total_minutes / 60