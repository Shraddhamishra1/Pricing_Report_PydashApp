import numpy as np
import pandas as pd
import os
import io
import regex as re

def generate_dataframe_YT06(decoded1, filename1,ppt_excel_path,MY05_additivecost_path,MY08_additivecost_path):

    if 'csv' in ppt_excel_path:
        ppt_excel = pd.read_csv(ppt_excel_path)
    elif 'xls' in ppt_excel_path:
        ppt_excel = pd.read_excel(ppt_excel_path, engine='openpyxl', dtype='object', sheet_name="Additive - YT06")

        ppt_excel = split_rows(ppt_excel, "Material")
        ppt_excel['New_TP'] = ppt_excel['Current_TP'].apply(extract_rate)
        ppt_excel = ppt_excel.drop_duplicates(subset='Material', keep='first')
    
    if 'csv' in MY05_additivecost_path:
        MY05_additivecost = pd.read_csv(MY05_additivecost_path)
    elif 'xls' in MY05_additivecost_path:
        MY05_additivecost = pd.read_excel_file(MY05_additivecost_path)

    if 'csv' in MY08_additivecost_path:
        MY08_additivecost = pd.read_csv(MY08_additivecost_path)
    elif 'xls' in MY08_additivecost_path:
        MY08_additivecost = pd.read_excel_file(MY08_additivecost_path)

    # # Read depot/plant mapping file
    # if 'csv' in ppt_excel_filename:
    #     ppt_excel = pd.read_csv(io.StringIO(ppt_excel_content.decode('utf-8')))
    #     ppt_excel = split_rows(ppt_excel, "Material")
    #     ppt_excel['New_TP'] = ppt_excel['Current_TP'].apply(extract_rate)
    #     ppt_excel = ppt_excel.drop_duplicates(subset='Material', keep='first')
        
    # elif 'xls' in ppt_excel_path:
    #     ppt_excel = pd.read_excel(io.BytesIO(ppt_excel_content), engine='openpyxl', dtype='object', sheet_name="Additive - YT06")
        
    # ------------------------------------------------------- 
    # if 'csv' in MY05_additivecost_filename:
    #     MY05_additivecost = pd.read_csv(io.StringIO(MY05_additivecost_content.decode('utf-8')))

    # elif 'xls' in MY05_additivecost_filename:
    #     MY05_additivecost = pd.read_excel(io.BytesIO(MY05_additivecost_content),header=1)
    # --------------------------------------------------------
    
    # if 'csv' in MY08_additivecost_filename:
    #     MY08_additivecost = pd.read_csv(io.StringIO(MY08_additivecost_content.decode('utf-8')))
        
    # elif 'xls' in MY08_additivecost_filename:
    #     MY08_additivecost = pd.read_excel(io.BytesIO(MY08_additivecost_content),header=1)
        
    # ----------------------------------------------------------------
    # Define the functions
    def split_rows(df, column):
        new_rows = []
        for index, row in df.iterrows():
            if '/' in row[column]:
                values = row[column].split('/')
                for value in values:
                    new_row = row.copy()
                    new_row[column] = value
                    new_rows.append(new_row)
            else:
                new_rows.append(row)
        return pd.DataFrame(new_rows)
    
    ppt_excel = split_rows(ppt_excel, "Material")
    ppt_excel['New_TP'] = ppt_excel['Current_TP'].apply(extract_rate)
    ppt_excel = ppt_excel.drop_duplicates(subset='Material', keep='first')

    def extract_rate(text):
        # Ensure the input is a string
        if not isinstance(text, str):
            text = str(text)
        
        match = re.search(r'\b(\d+\.\d+)\b', text)
        if match:
            return match.group(1)
        return None

    def grade_conditions(df):
        conditions = [
            df['Material Desc'].str.contains('ULG 95', na=False),
            df['Material Desc'].str.contains('ULG 97', na=False),
            df['Material Desc'].str.contains('ULG 95', na=False),
            df['Material Desc'].str.contains('AGO', na=False),
            df['Material Desc'].str.contains('VPR', na=False),
            df['Material Desc'].str.contains('GO', na=False),
            df['Material Desc'].str.contains('Kero', na=False),
            df['Material Desc'].str.contains('Gasoil', na=False),
            df['Material Desc'].str.contains('Jet A-1', na=False),
            df['Material Desc'].str.contains('ULG98', na=False)
        ]
        values = ['U95', 'U97', 'U95', 'GO', 'VPR', 'GO', 'Kero', 'GO', 'Jet A1', 'U98']

        df['Material'] = np.select(conditions, values, default=df['Material Desc'])
        return df

    def replace_rate_if_not_equal(df):
        df['Value'] = np.where(df['Value'] != df['New_TP'], df['New_TP'], df['Value'])
        return df

    def correct_rate(MY08_additivecost, MY05_additivecost, output_filename):            
        # Function to process each DataFrame
        def process_df(df):
            grade_conditions(df)
            df['Material'] = df['Material'].str.strip()
            ppt_excel['Material'] = ppt_excel['Material'].str.strip()
            merged_df = pd.merge(df, ppt_excel[['Material', 'New_TP']], on='Material', how='left')
            df_updated = replace_rate_if_not_equal(merged_df)
            df_updated.drop(columns=['Material', 'New_TP'], inplace=True)
            return df_updated

        # Process each DataFrame
        df_updated_MY08 = process_df(MY08_additivecost)
        df_updated_MY05 = process_df(MY05_additivecost)

        return df_updated_MY08, df_updated_MY05,ppt_excel
    
    return correct_rate(MY08_additivecost, MY05_additivecost, 'YT06_cost_update')