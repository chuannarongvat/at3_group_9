import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
import datetime
import sys
import traceback
pd.set_option('display.max_column', 100)
import time
import re


## Space for functions

def convert_to_epoch(df):
    depart_time = []  # Initialize the list to store departure times
    depttime=df['segmentsDepartureTimeRaw']
    for depttime in depttime :
        ts = pd.Timestamp(depttime)
        Hour = int(ts.hour)
        Minute = int(ts.minute)
        depart_time.append(f"{Hour:02d}:{Minute:02d}")  # Format the time as HH:MM
    df['depart_time'] = depart_time # Create a DataFrame from the list
        
    return df



def convert_travel_time(df):
    # Define the duration string
    duration_str = df['travelDuration']
    total_minutes=[]
    for duration in duration_str:
        # Use regular expressions to extract hours and minutes
        hours_match = re.search(r'(\d+)H', duration)
        minutes_match = re.search(r'(\d+)M', duration)
        # Initialize variables for hours and minutes
        hours = 0
        minutes = 0
        # If the matches are found, convert them to integers
        if hours_match:
            hours = int(hours_match.group(1))
            if minutes_match:
                minutes = int(minutes_match.group(1))
        # Calculate the total duration in minutes
        total_minutes.append(hours * 60 + minutes)
    
    df['travelDuration_minutes']=total_minutes
    return df


#Function to create parquet files
def process_and_save_csv(input_csv, output_parquet):
    output_path= "../data/processed/"
    df = pd.read_csv(input_csv, low_memory=False)

    df_itenary_cp = df[['searchDate', 'flightDate', 'startingAirport',
                       'destinationAirport', 'travelDuration', 'isBasicEconomy',
                       'isRefundable', 'isNonStop', 'totalFare', 'totalTravelDistance',
                       'segmentsDepartureTimeRaw', 'segmentsAirlineCode', 'segmentsCabinCode']].copy()

    df_itenary_cp['totalTravelDistance'] = df_itenary_cp['totalTravelDistance'].fillna('PT0H0M')
    df_itenary_cp['searchDate'] = pd.to_datetime(df_itenary_cp['searchDate'].str.replace('-', ''),
                                                 format='%Y%m%d', errors='coerce')
    df_itenary_cp['flightDate'] = pd.to_datetime(df_itenary_cp['flightDate'].str.replace('-', ''),
                                                 format='%Y%m%d', errors='coerce')
    df_itenary_cp['segmentsCabinCode'] = df_itenary_cp['segmentsCabinCode'].str.replace('|', ',').str.split(',').str[0]
    df_itenary_cp['segmentsDepartureTimeRaw'] = pd.to_datetime(
        df_itenary_cp['segmentsDepartureTimeRaw'].str.replace('|', ',').str.split(',').str[0],
        format='%Y-%m-%dT%H:%M:%S.%f%z', errors='coerce')

    df_itenary_cp['segmentsAirlineCode'] = df_itenary_cp['segmentsAirlineCode'].str.replace('|', ',').str.split(',').str[0]

    df_itenary_cp = df_itenary_cp.dropna()
    df_itenary_cp = convert_to_epoch(df_itenary_cp)
    df_itenary_cp = convert_travel_time(df_itenary_cp)

    df_itenary_cp = df_itenary_cp[['searchDate', 'flightDate', 'startingAirport', 'destinationAirport',
                                   'travelDuration_minutes', 'isBasicEconomy', 'isRefundable', 'isNonStop',
                                   'totalFare', 'totalTravelDistance', 'depart_time',
                                   'segmentsAirlineCode', 'segmentsCabinCode']]

    df_itenary_cp.to_parquet(output_path+output_parquet, index=False)

# Example usage for processing multiple CSV files
process_and_save_csv('../data/raw/DEN_full.csv','DEN_full.parquet')
process_and_save_csv('../data/raw/MIA_full.csv','MIA_full.parquet')
process_and_save_csv('../data/raw/LAX_full.csv','LAX_full.parquet')
process_and_save_csv('../data/raw/CLT_full.csv','CLT_full.parquet')
process_and_save_csv('../data/raw/BOS_full.csv','BOS_full.parquet')
process_and_save_csv('../data/raw/ATL_full.csv','ATL_full.parquet')
process_and_save_csv('../data/raw/SFO_full.csv','SFO_full.parquet')
process_and_save_csv('../data/raw/EWR_full.csv','EWR_full.parquet')
process_and_save_csv('../data/raw/ORD_full.csv','ORD_full.parquet')
process_and_save_csv('../data/raw/LGA_full.csv','LGA_full.parquet')
process_and_save_csv('../data/raw/DFW_full.csv','DFW_full.parquet')
process_and_save_csv('../data/raw/IAD_full.csv','IAD_full.parquet')
process_and_save_csv('../data/raw/OAK_full.csv','OAK_full.parquet')
process_and_save_csv('../data/raw/PHL_full.csv','PHL_full.parquet')
process_and_save_csv('../data/raw/JFK_full.csv','JFK_full.parquet')
process_and_save_csv('../data/raw/DTW_full.csv','DTW_full.parquet')





