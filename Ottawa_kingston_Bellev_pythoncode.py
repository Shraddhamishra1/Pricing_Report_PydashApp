import pandas as pd
import numpy as np
import io

def generate_dataframe_Ottawa_KgsBellev(ottawa_KgBlv_GsapData_content, ottawa_KgBlv_GsapData_filename, Ottawa_kgsBlv_TP):
    # Read the data based on the file type
    if 'csv' in ottawa_KgBlv_GsapData_filename:
        Ottawa_KgBlv_GsapData = pd.read_csv(io.StringIO(ottawa_KgBlv_GsapData_content.decode('utf-8')))
    elif 'xls' in ottawa_KgBlv_GsapData_filename:
        Ottawa_KgBlv_GsapData = pd.read_excel(io.BytesIO(ottawa_KgBlv_GsapData_content))
    
    # Process Material and Plant columns
    print("Processing Material and Plant columns...")
    Ottawa_KgBlv_GsapData['Material'] = Ottawa_KgBlv_GsapData['Material Desc'].apply(lambda x: str(x)[3:6] if not pd.isnull(x) else '')
    Ottawa_KgBlv_GsapData['Plant'] = Ottawa_KgBlv_GsapData['Varkey'].apply(lambda x: str(x)[4:8] if not pd.isnull(x) else '')

    # Define the conditions and corresponding values
    conditions = [
        Ottawa_KgBlv_GsapData['Plant'].isin(["C182", "C503", "C589"]),
        Ottawa_KgBlv_GsapData['Plant'].isin(["C131", "C175", "C178", "C349", "C594", "C210", "C123"]),
        Ottawa_KgBlv_GsapData['Plant'].isin(["C136", "C137"]),
        Ottawa_KgBlv_GsapData['Plant'].isin(["C134", "C177"]),
        Ottawa_KgBlv_GsapData['Plant'].isin(["C121", "C592"]),
        Ottawa_KgBlv_GsapData['Plant'].isin(["C100", "C101"]),
        Ottawa_KgBlv_GsapData['Plant'].isin(["C142", "C143", "C354", "C181"]),
        Ottawa_KgBlv_GsapData['Plant'] == ""
    ]

    choices = ["KAM", "OTT", "KEELE", "SSM", "TBAY", "REF", "WPG", ""]

    # Apply the conditions using numpy.select 
    print("Applying conditions to determine regions...")
    Ottawa_KgBlv_GsapData['Region'] = np.select(conditions, choices, default="NG")
    Ottawa_KgBlv_GsapData = Ottawa_KgBlv_GsapData[Ottawa_KgBlv_GsapData['Region'] == 'OTT']

    # Apply the logic for MAT Sum
    print("Applying logic for MAT Sum...")
    Ottawa_KgBlv_GsapData['MAT Sum'] = Ottawa_KgBlv_GsapData['Material'].apply(lambda x: 'GAS' if x == 'ULG' else ('ULSD' if x in ['DHO', 'AGO', 'KER', 'IGO'] else 'Other'))

    # Function to calculate New_TPValue
    def calculate_value(row):
        if row['MAT Sum'] == 'Other':
            return 0
        elif row['MAT Sum'] == 'GAS':
            return Ottawa_kgsBlv_TP.loc[Ottawa_kgsBlv_TP['Plant'] == row['Plant'], 'GAS_TP Value'].values[0] * 10
        elif row['MAT Sum'] == 'ULSD':
            return Ottawa_kgsBlv_TP.loc[Ottawa_kgsBlv_TP['Plant'] == row['Plant'], 'Diesel_TP Value'].values[0] * 10

    # Apply the calculate_value function
    print("Calculating New_TPValue...")
    Ottawa_KgBlv_GsapData['New_TPValue'] = Ottawa_KgBlv_GsapData.apply(calculate_value, axis=1)
    Ottawa_KgBlv_GsapData['Value'] = Ottawa_KgBlv_GsapData['New_TPValue']
    Ottawa_KgBlv_GsapData['Sequence No'] = range(1, len(Ottawa_KgBlv_GsapData) + 1)

    # Drop unnecessary columns
    print("Dropping unnecessary columns...")
    Ottawa_KgBlv_GsapData.drop(columns=['Material', 'Plant', 'MAT Sum', 'New_TPValue', 'Region'], inplace=True)

    print('DataFrame successfully generated!')
    return Ottawa_KgBlv_GsapData

    

