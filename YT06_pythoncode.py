import numpy as np
import pandas as pd
import os
import io
import regex as re

def generate_dataframe_YT06(GSAP_data_content, GSAP_data_filename, ppt_excel):
    # Read the data based on the file type
    if 'csv' in GSAP_data_filename:
        df = pd.read_csv(io.StringIO(GSAP_data_content.decode('utf-8')))
    elif 'xls' in GSAP_data_filename:
        df = pd.read_excel(io.BytesIO(GSAP_data_content))

    # Function to split rows based on a delimiter
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

    # Function to extract rate from text
    def extract_rate(text):
        # Ensure the input is a string
        if not isinstance(text, str):
            text = str(text)
        
        match = re.search(r'\b(\d+\.\d+)\b', text)
        if match:
            return match.group(1)
        return None

    # Split rows in ppt_excel and extract new rates
    ppt_excel = split_rows(ppt_excel, "Material")
    ppt_excel['New_TP'] = ppt_excel['Current_TP'].apply(extract_rate)
    ppt_excel = ppt_excel.drop_duplicates(subset='Material', keep='first')

    # Function to apply grade conditions
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

    # Function to replace rate if not equal
    def replace_rate_if_not_equal(df):
        df['Value'] = np.where(df['Value'] != df['New_TP'], df['New_TP'], df['Value'])
        return df

    # Function to process the DataFrame
    def process_df(df):
        print("Applying grade conditions...")
        grade_conditions(df)
        df['Material'] = df['Material'].str.strip()
        ppt_excel['Material'] = ppt_excel['Material'].str.strip()
        print("Merging dataframes...")
        merged_df = pd.merge(df, ppt_excel[['Material', 'New_TP']], on='Material', how='left')
        print("Replacing rates where necessary...")
        df_updated = replace_rate_if_not_equal(merged_df)
        df_updated.drop(columns=['Material', 'New_TP'], inplace=True)
        return df_updated

    # Process the DataFrame
    print("Processing the DataFrame...")
    YT06_output = process_df(df)
    print('YT06 output successfully generated !!')

    return YT06_output