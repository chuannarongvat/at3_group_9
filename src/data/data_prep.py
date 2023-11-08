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
    
    plt.figure(figsize=(20, 6))
    sns.barplot(data=df, x=x, y=y, palette='ch:.25')
    plt.xticks(rotation=45, ha='right')
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

def calculate_diff_in_minutes(row):
    timestamps = row.split('||')
    if len(timestamps) == 2:
        return abs(int(timestamps[1]) - int(timestamps[0])) / 60
    else:
        return None
    
def split_column(df, column_name):
    if column_name in df.columns:
        df[[column_name + '_1', column_name + '_2']] = df[column_name].str.split('||', expand=True)
    else:
        print(f"The column '{column_name}' does not exist in the DataFrame.")
    
    return df

def split_column(df, column_name):
    if column_name in df.columns:
        df[[column_name + '_1', column_name + '_2']] = df[column_name].str.split('\|\|', n=1, expand=True)
    else:
        print(f"The column '{column_name}' does not exist in the DataFrame.")
    
    return df

def split_all_columns(df):
    for col_name in df.columns:
        if df[col_name].dtype == 'object' and df[col_name].str.contains('\|\|').any():
            df[[col_name + '_1', col_name + '_2']] = df[col_name].str.split('\|\|', n=1, expand=True)
            df.drop(col_name, axis=1, inplace=True)
    return df

def calculate_flight_duration(df, dep_col_1, arr_col_1, dep_col_2, arr_col_2):
    df[dep_col_1] = df[dep_col_1].astype(int)
    df[arr_col_1] = df[arr_col_1].astype(int)
    df[dep_col_2] = df[dep_col_2].astype(int)
    df[arr_col_2] = df[arr_col_2].astype(int)
    
    df['flight_duration_1'] = (df[arr_col_1] - df[dep_col_1]) / 60
    
    df['flight_duration_2'] = (df[arr_col_2] - df[dep_col_2]) / 60
    
    return df

def plot_fare_histograms_by_destination(df, start_airport, dest_airport_col, fare_col, hue_col=None, bins=20):
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    df_filtered = df[df['startingAirport'] == start_airport]
    
    g = sns.FacetGrid(df_filtered, col=dest_airport_col, col_wrap=5, sharex=False, sharey=False, hue=hue_col)
    
    hist_kwargs = {'bins': bins, 'kde': False}
    if hue_col:
        hist_kwargs['hue'] = df_filtered[hue_col]
    
    g = g.map(sns.histplot, fare_col, **hist_kwargs)
    
    g.fig.suptitle(f'Histograms of Total Fare from {start_airport} Airport', y=1.02)
    g.set_axis_labels('Total Fare ($)', 'Frequency')
    
    for ax in g.axes.flat:
        for label in ax.get_xticklabels():
            label.set_rotation(45)
    
    if hue_col:
        g.add_legend()
        
    g.tight_layout()
    plt.show()
    
def plot_fare_trends_by_date_and_destination(df, start_airport, dest_airport_col, date_col, fare_col, hue_col, bins=20):
    import seaborn as sns
    import matplotlib.pyplot as plt
    import pandas as pd

    df[date_col] = pd.to_datetime(df[date_col])

    df_filtered = df[df['startingAirport'] == start_airport]
    
    g = sns.FacetGrid(df_filtered, col=dest_airport_col, col_wrap=5, sharex=False, sharey=False, hue=hue_col, legend_out=True)
    
    g = g.map(sns.lineplot, date_col, fare_col)
    
    g.fig.suptitle(f'Fare Trends over Flight Dates from {start_airport} Airport', y=1.02)
    g.set_axis_labels('Flight Date', 'Total Fare')
    
    for ax in g.axes.flat:
        for label in ax.get_xticklabels():
            label.set_rotation(45)
    
    g.add_legend(title=hue_col)
    
    plt.tight_layout()
    plt.show()
    
def plot_distance_histograms_by_destination(df, start_airport, dest_airport_col, dist_col, hue_col=None, bins=20):
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    df_filtered = df[df['startingAirport'] == start_airport]
    
    g = sns.FacetGrid(df_filtered, col=dest_airport_col, col_wrap=5, sharex=False, sharey=False, hue=hue_col)
    
    hist_kwargs = {'bins': bins, 'kde': False}
    if hue_col:
        hist_kwargs['hue'] = df_filtered[hue_col]
    
    g = g.map(sns.histplot, dist_col, **hist_kwargs)
    
    g.fig.suptitle(f'Histograms of Total Total Distance from {start_airport} Airport', y=1.02)
    g.set_axis_labels('Total Distance ($)', 'Frequency')
    
    for ax in g.axes.flat:
        for label in ax.get_xticklabels():
            label.set_rotation(45)
    
    if hue_col:
        g.add_legend()
        
    g.tight_layout()
    plt.show()
    
def plot_day_of_week_fare(df, start_airport, dest_airport_col, fare_col, bins=20):
    import seaborn as sns
    import matplotlib.pyplot as plt

    df_filtered = df[df['startingAirport'] == start_airport]

    g = sns.FacetGrid(df_filtered, col=dest_airport_col, col_wrap=5, sharex=False, sharey=False)

    def create_barplot(data, **kwargs):
        sns.barplot(data=data, x='day_of_week', y=fare_col, ax=plt.gca())

    g.map_dataframe(create_barplot, data=df_filtered)

    g.set_titles(col_template="{col_name} Airport")
    g.set_axis_labels('Day of the Week', f'Mean {fare_col}')
    
    g.fig.suptitle(f'Day of the Week Mean Fare from {start_airport} Airport', y=1.02)

    for ax in g.axes.flat:
        for label in ax.get_xticklabels():
            label.set_rotation(45)

    g.tight_layout()
    plt.show()
    
def plot_day_of_week_fare_isnonstop(day_of_week_fare):
    import seaborn as sns
    import matplotlib.pyplot as plt

    ax = sns.barplot(x='day_of_week', y='totalFare', data=day_of_week_fare, hue='isNonStop', palette="ch:.25")

    ax.set(xlabel="Day of the Week", ylabel="Mean Total Fare ($)", title='Day of the Week Mean Fare')

    plt.xticks(rotation=45)
    plt.legend(title='isNonStop', loc='upper left', bbox_to_anchor=(1, 1))
    
    plt.tight_layout()
    
    plt.show()
    
def plot_day_of_week_count(df, start_airport, dest_airport_col, hue_col, bins=20):
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    df_filtered = df[df['startingAirport'] == start_airport]

    g = sns.FacetGrid(df_filtered, col=dest_airport_col, col_wrap=5, sharex=False, sharey=False)

    def create_countplot(data, **kwargs):
        sns.countplot(data=data, x='day_of_week', hue=hue_col, palette='ch:.25', ax=plt.gca())

    g.map_dataframe(create_countplot, data=df_filtered)

    g.set_titles(col_template="{col_name} Airport")
    g.set_axis_labels('Day of the Week', 'Count')

    g.fig.suptitle(f'Count of {hue_col} from {start_airport} Airport', y=1.02)

    for ax in g.axes.flat:
        for label in ax.get_xticklabels():
            label.set_rotation(45)

    g.tight_layout()

    plt.legend(title=hue_col, bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.show()    
    
def date_to_day_of_week(df, date_col):
    try:
        df[date_col] = pd.to_datetime(df[date_col])
        
        df['day_of_week'] = df[date_col].dt.strftime('%A')
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df['day_of_week'] = pd.Categorical(df['day_of_week'], categories=day_order, ordered=True)
    except ValueError:
        print("Invalid Date Format")
    
    return df

def date_to_numeric_day_of_week(df, date_col):
    try:
        df[date_col] = pd.to_datetime(df[date_col])
        df['day_of_week'] = df[date_col].dt.dayofweek
    except ValueError:
        print("Invalid Date Format")
    
    return df

def convert_to_km(df, distance):
    df[distance] = df[distance].astype(int) * 1.60934
    
    return df

def extract_time(df, column_name):
    try:
        df[column_name] = pd.to_datetime(df[column_name], utc=True)
        
        df['departureTime_fraction'] = df[column_name].dt.hour / 24 + df[column_name].dt.minute / (24 * 60)
        df['departureTime'] = df[column_name].dt.strftime('%H:%M')
    except Exception as e:
        print("Error:", e)
    
    return df

def create_time_bins(df, column_name, bin_size_minutes=60, bin_labels=None):
    df['departureTime_convert'] = pd.to_datetime(df[column_name], format='%H:%M')
    
    df['hour'] = df['departureTime_convert'].dt.hour
    df['minute'] = df['departureTime_convert'].dt.minute
    
    df['total_minutes'] = df['hour'] * 60 + df['minute']
    
    bin_edges = list(range(0, 1441, bin_size_minutes))
    
    if bin_labels:
        df['{}_bins'.format('departureTime_convert')] = pd.cut(df['total_minutes'], bins=bin_edges, labels=bin_labels)
    else:
        df['{}_bins'.format('departureTime_convert')] = pd.cut(df['total_minutes'], bins=bin_edges)
    
    df.drop(['departureTime_convert', 'hour', 'minute', 'total_minutes'], axis=1, inplace=True)
    
    return df

def transform_segments_cabin_code(segment):
    segments = segment.split('||')
    unique_segments = list(set(segments))
    
    if len(unique_segments) == 1:
        return unique_segments[0]
    else:
        return 'mix'