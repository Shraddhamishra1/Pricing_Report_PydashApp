import numpy as np
import pandas as pd
import io

def generate_dataframe_YT07(GSAP_data_content, GSAP_data_filename, PTtransfer, depot_mapping):
    
    # Read the data based on the file type
    if 'csv' in GSAP_data_filename:
        df = pd.read_csv(io.StringIO(GSAP_data_content.decode('utf-8')))
    elif 'xls' in GSAP_data_filename:
        df = pd.read_excel(io.BytesIO(GSAP_data_content))

    # Extract the latest rates from PTtransfer
    latest_rates = PTtransfer.iloc[:, [0, 3]]
    latest_rates.columns = ['PT PlantName', 'Latest_rate']

    # Function to replace rate if not equal
    def replace_rate_if_not_equal(df):
        df['Value'] = df.apply(lambda row: row['Latest_rate'] if row['Value'] != row['Latest_rate'] else row['Value'], axis=1)
        return df

    # Function to process the DataFrame
    def process_df(df):
        print("Extracting Depot ID...")
        df['Depot_ID'] = df['Varkey'].str[4:8]  # to get depot ID
        print("Merging with depot mapping to get plant name...")
        merged_df = pd.merge(df, depot_mapping[['Depot_ID', 'PT PlantName']], on='Depot_ID', how='left')  # merging to get plant name
        print("Merging with latest rates to get latest transfer price...")
        merged_df = pd.merge(merged_df, latest_rates, on='PT PlantName', how='left')  # merging to get latest transfer price
        print("Replacing rates where necessary...")
        df_updated = replace_rate_if_not_equal(merged_df)
        df_updated.drop(columns=['Depot_ID', 'PT PlantName', 'Latest_rate'], inplace=True)
        return df_updated

    # Process the DataFrame
    print("Processing the DataFrame...")
    YT07_output = process_df(df)
    print('YT07 output successfully generated !!')

    return YT07_output