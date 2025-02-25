# %%
import numpy as np
import pandas as pd
import os
import io

def generate_dataframe_YT07(MY05_PT_UpdateM05_content, MY05_PT_UpdateM05_filename,MY08_PT_UpdateM05_content,MY08_PT_UpdateM05_filename, ppt_excel_content,ppt_excel_filename, depot_mapping_content, depot_mapping_filename):
    
    # Read depot/plant mapping file
    if 'csv' in ppt_excel_filename:
        PTtransfer = pd.read_csv(io.StringIO(ppt_excel_content.decode('utf-8')))
    elif 'xls' in ppt_excel_filename:
        PTtransfer = pd.read_excel(io.BytesIO(ppt_excel_content), engine='openpyxl', dtype='object', sheet_name="Primary Transport - YT07")
    # ------------------------------------------------------- 
    if 'csv' in depot_mapping_filename:
        depot_mapping = pd.read_csv(io.StringIO(depot_mapping_content.decode('utf-8')))
    elif 'xls' in depot_mapping_filename:
        depot_mapping = pd.read_excel(io.BytesIO(depot_mapping_content), engine='openpyxl', dtype='object', sheet_name="Depot Mapping")
    # --------------------------------------------------------
    if 'csv' in MY05_PT_UpdateM05_filename:
        PTupdateMY05 = pd.read_csv(io.StringIO(MY05_PT_UpdateM05_content.decode('utf-8')))
    elif 'xls' in MY05_PT_UpdateM05_filename:
        PTupdateMY05 = pd.read_excel(io.BytesIO(MY05_PT_UpdateM05_content),header=1)
    # ----------------------------------------------------
    if 'csv' in MY08_PT_UpdateM05_filename:
        PTupdateMY08 = pd.read_csv(io.StringIO(MY08_PT_UpdateM05_content.decode('utf-8')))    
    elif 'xls' in MY08_PT_UpdateM05_filename:
        PTupdateMY08 = pd.read_excel(io.BytesIO(MY08_PT_UpdateM05_content),header=1)
    # ----------------------------------------------------------------
    latest_rates=PTtransfer.iloc[:,[0,3]]
    latest_rates.columns=['PT PlantName','Latest_rate']

    def replace_rate_if_not_equal(df):
        df['Value'] = df.apply(lambda row: row['Latest_rate'] if row['Value'] != row['Latest_rate'] else row['Value'], axis=1)
        return df
    
    def correct_rate(PTupdateMY05, PTupdateMY08, output_filename):            
        # Function to process each DataFrame
        def process_df(df):
            df['Depot_ID']=df['Varkey'].str[4:8]# to get depot ID
            merged_df = pd.merge(df, depot_mapping[['Depot_ID', 'PT PlantName']], on='Depot_ID', how='left')# merging to get plant name
            merged_df = pd.merge(merged_df, latest_rates, on='PT PlantName', how='left')#merging to get latest transfer price
            df_updated=replace_rate_if_not_equal(merged_df)
            df_updated.drop(columns=['Depot_ID','PT PlantName','Latest_rate'], inplace=True)
            return df_updated
        
        df_updated_MY05 = process_df(PTupdateMY05)
        df_updated_MY08 = process_df(PTupdateMY08)

        return df_updated_MY05, df_updated_MY08
    
    return correct_rate(PTupdateMY05, PTupdateMY08, 'YT07_cost_update')