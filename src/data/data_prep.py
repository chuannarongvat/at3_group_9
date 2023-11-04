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