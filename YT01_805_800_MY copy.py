import os
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash import dash_table
from dash import callback, State
import plotly.graph_objs as go
from getpass import getuser
import pandas as pd
import numpy as np
from os import walk
import glob
import base64
import datetime as dt
import io
import regex as re

# def generate_dataframe(gs_report_content, gs_report_filename, mapping_file_content, mapping_file_filename, ppt_excel_content, ppt_excel_filename, depot_mapping_content, depot_mapping_filename):
def generate_dataframe(gs_report_content, gs_report_filename, Mapping_quotation_codes, depot_mapping,MY_Historical_values):

    print("#######################################")
    # T&S - TAKEN DEPO , MATERIAL MAPING 
    if 'csv' in gs_report_filename:
        df = pd.read_csv(io.StringIO(gs_report_content.decode('utf-8')))
    elif 'xls' in gs_report_filename:
        df = pd.read_excel(io.BytesIO(gs_report_content))

    # if 'csv' in mapping_file_path:
    #     map_df = pd.read_csv(mapping_file_path)
    # elif 'xls' in mapping_file_path:
    #     map_df = pd.read_excel(mapping_file_path, engine='openpyxl', dtype='object', header=1)

    # if 'csv' in depot_mapping_path:
    #     depot_df1 = pd.read_csv(depot_mapping_path)
    # elif 'xls' in depot_mapping_path:
    #     depot_df1 = pd.read_excel(depot_mapping_path, engine='openpyxl', dtype='object', sheet_name="Depot Mapping")
        
        map_df = Mapping_quotation_codes
        depot_df1 = depot_mapping
        tp_template = MY_Historical_values

    # def read_excel_file(ppt_excel_path):
    #     xls = pd.ExcelFile(ppt_excel_path, engine='openpyxl')
    #     sheet_dict = {sheet_name: pd.read_excel(xls, sheet_name=sheet_name, dtype='object') for sheet_name in xls.sheet_names}
    #     return sheet_dict

    # def get_sheet_df(sheet_dict, sheet_name):
    #     return sheet_dict.get(sheet_name)
    
    # if 'csv' in ppt_excel_path:
    #     tp_template = pd.read_csv(ppt_excel_path)
    # elif 'xls' in ppt_excel_path:
    #     tp_template = read_excel_file(ppt_excel_path)
# --------------------------------------------------------------------------------------------
        # tp_template = pd.read_excel(ppt_excel_path, engine='openpyxl', dtype='object')

    
    # def process_excel_file(file_path):
    #     if file_path.endswith('.csv'):
    #         tp_template = pd.read_csv(file_path)
    #     elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
    #         tp_template = read_excel_file(file_path)
    #     else:
    #         raise ValueError("Unsupported file format")
    #     return tp_template

    # tp_template = process_excel_file(file_path)
    
        
    # # Read mapping file for quotation codes
    # if 'csv' in mapping_file_filename:
    #     map_df = pd.read_csv(io.StringIO(mapping_file_content.decode('utf-8')))
    # elif 'xls' in mapping_file_filename:
    #     map_df = pd.read_excel(io.BytesIO(mapping_file_content), header=1)
    
    # Function to read the Excel file and store all sheets in a dictionary
    # def read_excel_file(ppt_excel_content):
    #     excel_content = io.BytesIO(ppt_excel_content)
    #     xls = pd.ExcelFile(excel_content, engine='openpyxl')
    #     sheet_dict = {sheet_name: pd.read_excel(xls, sheet_name=sheet_name, dtype='object') for sheet_name in xls.sheet_names}
    #     return sheet_dict

    # # Function to get a specific sheet DataFrame from the dictionary
    # def get_sheet_df(sheet_dict, sheet_name):
    #     return sheet_dict.get(sheet_name)

    # # Assuming ppt_excel_filename and ppt_excel_content are defined
    # if 'csv' in ppt_excel_filename:
    #     tp_template = pd.read_csv(io.StringIO(ppt_excel_content.decode('utf-8')))
        
    # elif 'xls' in ppt_excel_filename:
    #     # Read the entire Excel file into a dictionary of DataFrames
    #     tp_template = read_excel_file(ppt_excel_content)
         
    # # Read depot/plant mapping file
    # if 'csv' in depot_mapping_filename:
    #     depot_df1 = pd.read_csv(io.StringIO(depot_mapping_content.decode('utf-8')))
        
    # elif 'xls' in depot_mapping_filename:
    #     depot_df1 = pd.read_excel(io.BytesIO(depot_mapping_content), engine='openpyxl', dtype='object', sheet_name="Depot Mapping")
        
    
    def process_data(df, map_df):
        # Clean map_df and create Key column
        map_df = map_df.dropna(how='all').copy()
        map_df['Key'] = map_df['Quotation source'] + map_df['Quotation type'] + map_df['Quotation number']
    
        # Create Key column in df
        df['Key'] = df['Quotation source'] + df['Quotation type'] + df['Quotation number']
        df['Start Date'] = df['Start Date'].apply(lambda x: pd.NaT if x == "" else pd.to_datetime(x, format="%Y%m%d"))
        # Split Varkey to get CompanyCode, PlantCode, and MaterialCode
        df['CompanyCode'] = df['Varkey'].str.slice(0, 4)
        df['PlantCode'] = df['Varkey'].str.slice(4, 8)
        df['MaterialCode'] = df['Varkey'].str.slice(-9)
        # Merge df with map_df on Key column
        merged_df = pd.merge(df, map_df[['Key', 'User Interface']], on='Key', how='left')
        return merged_df
    
    def process_ppt_excel(df, yt_one_sel):
       """
       Processes the df DataFrame by resetting the index, stripping white spaces,
       and replacing 'no change' in the 'Current_TP' column with the value from 'Old_TP'.
       This runs for each material selected in the 'yt_one' list.

       Parameters:
       df (pd.DataFrame): The input DataFrame to be processed.

       Returns:
       pd.DataFrame: The processed DataFrame.
       """
       # Rename columns
       df.columns = ['Source', 'Grade at Location', 'Old_TP', 'Current_TP', 'Period']
       # Reset index and strip white spaces
       df.reset_index(drop=True, inplace=True)
       df['Grade at Location'] = df['Grade at Location'].str.strip()
       df['Old_TP'] = df['Old_TP'].str.strip()
       df['Current_TP'] = df['Current_TP'].str.strip()
       
       # Replace 'no change' in Current_TP column with Old_TP
       df['Current_TP'] = np.where(df['Current_TP'].str.lower() == 'no change', df['Old_TP'], df['Current_TP'])

       # replace '+ dem' with '& dem'
       df['Current_TP'] = df['Current_TP'].str.replace(r'\+ dem','& dem', regex=True)
       
       df = df.loc[df['Period']==df['Period'].max()].copy()
       df['sheet_name'] = yt_one_sel
       
       # Split 'Grade at Location' column into 'Plant', 'Grade', and 'FOB' columns
       if yt_one_sel == 'U95':
           df[['Plant', 'Grade', 'FOB']] = df['Grade at Location'].str.split("_", expand=True)
       
       elif yt_one_sel == 'U97':
           df['FOB']=""
           df[['Plant', 'Grade']] = df['Grade at Location'].str.split("_", expand=True)

       else:
           df[['Plant', 'Grade', 'FOB']] = df['Grade at Location'].str.split("_", expand=True)
    
       # replace brackets with empty string
       df['Plant'] = df['Plant'].str.replace("(", "").str.replace(")","") 
       # split on comma to get multiple plants
       df['Plant'] = df['Plant'].str.split(",") 
   
       #generate one line  for each plant
       df = df.explode('Plant') 
   
       # remove white spaces from plant name
       df['Plant'] = df['Plant'].str.strip(" ") 

       # create a list of charge component
       df['Charges']= df['Current_TP'].str.split("+")

       # Also remove 'Sabah' and Sarawak from Plant column only is sheet_name is E5 GO 10ppm
       if df['sheet_name'].unique() == "E5 GO 10ppm":
        df['Plant'] = df['Plant'].str.replace("Sabah", "").str.replace("Sarawak", "").str.replace("  ", " ").str.strip()
        df['Plant'] = df['Plant'].replace('Shell Westport', 'Westport')

       # reset index and drop the period column
       df.drop(columns=['Period'], inplace=True)
       df.reset_index(drop=True,inplace=True)
       df = df.explode('Charges')
       
       # check if col has currency or % values
       df['Curr_Per'] = df['Charges'].apply(lambda x: 'Yes' if  ("%")  in x else ("Yes" if  ("$") in x else ("Yes" if ('RM')  in x else "No")))
       df['Curr_Type'] = df['Charges'].apply(lambda x: "$/bbl" if  ("$") in x else ("RM/MT" if ('RM') in x else ""))

       # extract number before currency and % values
       df['Num_Extract'] = df['Charges'].str.extract('(\d+\.?\d*)')
       df['Charges'].str.extract('([0-9][/,.]\*[0-9]\*+)')

       # for currency and % maintain values as such, for others replace by 1
       df['Factor'] = np.where( df['Curr_Per']=='Yes', df['Num_Extract'], 1)

       # replace codes for GBI02, GSE01, JMI02. This is only for Gasoil
       if df['sheet_name'].unique() == "E5 GO 10ppm":
           df['Charges'] = df['Charges'].apply(lambda x: 'GBI02' if ('GBI02') in x else ( 'GSE01' if  ('GSE01') in x  else ('JMI02' if 'JMI02' in x else x)))

       # replace ICP Market 
       # this is only for Gasoil
       if df['sheet_name'].unique() == "E5 GO 10ppm":
        df['Charges'] = df['Charges'].str.replace('ICP GO Market Prem','GO ICP Weekly Mkt Prem')
        df['Charges'] = df['Charges'].str.replace('GO ICP Weekly Prem','GO ICP Weekly Mkt Prem')
       # create key
       df['Factor_Key'] = df['Plant'].str.strip().str.replace(" ","") + df['Charges'].str.strip().str.replace(" ","")
       df['Factor'] = df['Factor'].astype(float)
       df['Lines'] = df.groupby('Plant')['Plant'].transform('count')
       
       is_dataframe = isinstance(df, pd.DataFrame)
        # This will print True if df is a DataFrame, otherwise False
       return df
          
    def map_depot_to_plant(df):
        """
        Maps depot information to plant information by extracting and renaming relevant columns.

        Parameters:
        df (pd.DataFrame): The input DataFrame containing depot information.

        Returns:
        pd.DataFrame: A DataFrame with mapped depot to plant information.
        """
        plant_df = df[['Depot_ID', 'DF Plant', 'PlantName']].copy()
        plant_df['Plant_ID'] = plant_df['DF Plant'].apply(lambda x: x.split(" ")[0])
        plant_df = plant_df.rename(columns={'PlantName': 'Plant'})
        plant_df = plant_df[['Depot_ID', 'Plant']]
        return plant_df
    
    # MAP MATERIAL
    def map_material(df):
        """
        Maps material descriptions to standardized material codes.

        This function takes a DataFrame containing material descriptions and maps
        them to standardized material codes based on specific conditions. If a
        description does not match any of the predefined conditions, it retains
        its original description.

        Parameters:
        df (pd.DataFrame): A DataFrame containing a column 'Material Desc'
                                     with material descriptions.

        Returns:
        pd.DataFrame: The input DataFrame with an additional column 'Material_Final'
                  containing the mapped material codes.
        """
        conditions = [
            df['Material Desc'].str.contains('ULG 95', na=False),
            df['Material Desc'].str.contains('ULG 97', na=False),
            df['Material Desc'].str.contains('VPR', na=False),
            df['Material Desc'].str.contains('GO 10ppm', na=False),
            df['Material Desc'].str.contains('GO 10 ppm', na=False),
            df['Material Desc'].str.contains('Jet A-1', na=False)
        ]
        
        values = ['U95', 'U97', 'VPR', 'E5 GO 10ppm', 'E5 GO 10ppm', 'Jet A1']
        df['Material_Final'] = np.select(conditions, values, default=df['Material Desc'])
        return df
    
    # set columns to correct data types
    def convert_column_types(df_ref):
        """
        This function converts the data types of specific columns in a DataFrame.

        Parameters:
        df_ref (pd.DataFrame): The DataFrame containing the columns to be converted.

        Returns:
        pd.DataFrame: The DataFrame with the converted column types.
        """
        df_ref['Calculation factor 1'] = df_ref['Calculation factor 1'].astype(float)
        df_ref['Quotation number'] = df_ref['Quotation number'].astype(str)
        df_ref['User Interface'] = df_ref['User Interface'].astype(str)
        df_ref['Surcharge currency'] = df_ref['Surcharge currency'].astype(str)
        return df_ref
    
    
    def get_max_lines_per_sequence(df):
        """
    Get the maximum number of lines for each sequence number.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame containing 'Sequence No' and 'Formula term item number' columns.
    
    Returns:
    pd.DataFrame: DataFrame with an additional 'Max_Lines' column.
    """
        df['Max_Lines'] = df.groupby('Sequence No')['Formula term item number'].transform('max').astype(int)
        return df
    
    def mark_last_row(df):
        """
    Mark the last row in the DataFrame based on 'Formula term item number'.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame containing 'Formula term item number' column.
    
    Returns:
    pd.DataFrame: DataFrame with an additional 'Last_Row' column.
    """
        df['Formula term item number'].fillna(0, inplace=True)
        df['Last_Row'] = df.apply(lambda row: 'Last' if row['Formula term item number'] == 0 else "", axis=1)
        return df
    
    def check_max_lines(df):
        """
    Check the maximum number of lines in the GSAP file and the current TP file.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame containing 'Sequence No' and 'Formula term item number' columns.
    
    Returns:
    pd.DataFrame: DataFrame with an additional 'Max_Formula_Line' column.
    """
        df['Max_Formula_Line'] = df.groupby('Sequence No')['Formula term item number'].transform('max')
        return df
    
    
    def subset_data(df, material):
        """
    Subset the DataFrame only for the specified material.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame containing 'Material_Final' column.
    material (str): The material to filter the DataFrame by.
    
    Returns:
    pd.DataFrame: Subset DataFrame containing only the specified material.
    """
        df = df.loc[df['Material_Final'] == material, :].copy()
        return df
    
    
    def replace_nan_values(df, columns, replace_value='nan', new_value=np.NaN):
        """
        Replace specified values with new values in given columns.
        Parameters:
        df (pd.DataFrame): The input DataFrame.
        columns (list): List of columns to perform the replacement on.
    replace_value (str): The value to be replaced. Default is 'nan'.
    new_value: The new value to replace with. Default is np.NaN.
    
    Returns:
    pd.DataFrame: DataFrame with specified values replaced.
    """
        for column in columns:
            df[column] = df[column].replace(replace_value, new_value)
        return df
    
    
    def create_compare_column(df):
        """
    Create a compare column to check common elements between the GSAP data and the Excel TP input.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame containing 'Factor_Key', 'Surcharge currency', 'Last_Row', and 'Plant' columns.
    
    Returns:
    pd.DataFrame: DataFrame with an additional 'compare' column.
    """
        df['compare'] = df['Factor_Key'].combine_first(df['Surcharge currency'])
        df['compare'] = df['compare'].combine_first(df['Last_Row'])
        df['compare'] = df.apply(lambda row: row['Plant'] + row['compare'] if str(row['Surcharge currency']) != 'nan' else row['compare'], axis=1)
        return df
    
    
    def create_compare_column_tp_excel(df, currency_replacements=None, special_cases=None):
        """
        Create a compare column in the TP Excel sheet.
    
        Parameters:
        df (pd.DataFrame): The input DataFrame containing 'Curr_Type', 'Factor_Key', and 'Plant' columns.
        currency_replacements (dict): Dictionary of currency replacements. Default is {'$/bbl': 'USD', 'RM/MT': 'MYR'}.
        special_cases (dict): Dictionary of special case replacements. Default is {'ICP GO Market Prem': 'GO ICP Weekly Mkt Prem'}.
    
        Returns:
        pd.DataFrame: DataFrame with an additional 'compare' column.
        """
        if currency_replacements is None:
            currency_replacements = {'$/bbl': 'USD', 'RM/MT': 'MYR'}
        if special_cases is None:
            special_cases = {'ICP GO Market Prem': 'GO ICP Weekly Mkt Prem'}
        
        df_copy = df.copy()
        df_copy.replace("", np.NaN, inplace=True)
        df_copy.reset_index(inplace=True, drop=True)  # Reset index as combine_first does not work with duplicate indices
    
        df_copy['compare'] = df_copy['Curr_Type'].combine_first(df_copy['Factor_Key'])
        df_copy['compare'] = df_copy['compare'].replace(currency_replacements)
        df_copy['compare'] = df_copy['compare'].str.strip()
    
        for key, value in special_cases.items():
            df_copy.loc[df_copy['compare'] == key, 'compare'] = value
        
        df_copy['compare'] = df_copy.apply(lambda row: row['Plant'] + row['compare'] if str(row['Curr_Type']) != 'nan' else row['compare'], axis=1)
        return df_copy
    
    
    def update_rbdpo(df, biodiesel):
        """
    Updates the 'Surcharge' and 'Surcharge currency' columns in the df DataFrame based on conditions.

    This function performs the following steps:
    1. Iterates through each row in the df DataFrame.
    2. Checks if 'RBDPO' is in the 'Factor_Key' column and if the 'Plant' column does not contain 'Sabah' or 'Sarawak'.
    3. Updates the 'Surcharge' and 'Surcharge currency' columns based on the 'Grade at Location' in the biodiesel DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing gasoil data.
    biodiesel (pd.DataFrame): The processed DataFrame containing 'Grade at Location', 'Amount', and 'Currency' columns.

    Returns:
    pd.DataFrame: The updated df DataFrame with modified 'Surcharge' and 'Surcharge currency' columns.
    """
        # Ensure the 'Surcharge' column is of type float64
        df['Surcharge'] = df['Surcharge'].astype(float)     
        
        for i in range(len(df)):
            if 'RBDPO' in df.loc[i, 'Factor_Key'].strip():
                if 'RBDPO' in df.loc[i, 'Factor_Key']:
                    if (('Sabah') not in df.loc[i, 'Plant']) | (('Sarawak') not in df.loc[i, 'Plant']):
                        if df.loc[i + 1, 'Surcharge'] != biodiesel.loc[biodiesel['Grade at Location'] == "Pen. Msia", 'Amount'].values[0]:
                            df.loc[i + 1, 'Surcharge'] = biodiesel.loc[biodiesel['Grade at Location'] == "Pen. Msia", 'Amount'].values[0]
                            df.loc[i + 1, 'Surcharge currency'] = biodiesel.loc[biodiesel['Grade at Location'] == "Pen. Msia", 'Currency'].values[0]
                    else:
                        if (('Sabah') in df.loc[i, 'Plant']) | (('Sarawak') in df.loc[i, 'Plant']):
                            loc = df.loc[i, 'Plant']
                            if df.loc[i + 1, 'Surcharge'] != biodiesel.loc[biodiesel['Grade at Location'] == loc, 'Amount'].values[0]:
                                df.loc[i + 1, 'Surcharge'] = biodiesel.loc[biodiesel['Grade at Location'] == loc, 'Amount'].values[0]
                                df.loc[i + 1, 'Surcharge currency'] = biodiesel.loc[biodiesel['Grade at Location'] == loc, 'Currency'].values[0]
            
        # print(i, df.loc[i + 1, ['User Interface', 'Surcharge', 'Surcharge currency']])
        return df
    
    def update_calculation_factors(df, sel):
        """
    Updates the calculation factors in the DataFrame based on specific conditions.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing the data to be updated.

    Returns:
    pd.DataFrame: The updated DataFrame with modified calculation factors.
    """
        for i in range(len(df)):
            if (sel in df['Material_Final'][i]) & (sel !='E5 GO 10ppm'):
                if (df.loc[i, 'Surcharge'] == 0) & (df.loc[i, 'Quotation number'] not in ("")):
                    if (df.loc[i, 'Calculation factor 1'] != df.loc[i, 'Factor']) & (df.loc[i, 'Last_Row'] != 'Last'):
                        if (df.loc[i, 'Curr_Per'] == 'No'):
                            df.loc[i, 'Calculation factor 1'] = df.loc[i, 'Factor'] + df.loc[i, 'Oil_Loss_Correction']
                        else:
                            df.loc[i, 'Calculation factor 1'] = (df.loc[i, 'Factor'] / 100) + df.loc[i, 'Oil_Loss_Correction']
                        # if there is a change in Calculation factor 1, update the start date where formula term item number is 1
                        seq_no = df.loc[i, 'Sequence No']
                        df.loc[(df['Sequence No'] == seq_no) & (df['Formula term item number'] == 1), 'Start Date'] = dt.datetime.now().strftime("%Y%m%d")
                        
            elif (sel in df['Material_Final'][i]) & (sel=='E5 GO 10ppm'):
                if (df.loc[i,'Surcharge']==0) &  (df.loc[i,'Quotation number'] not in ("")):
                    if ('GBI02'  in (df.loc[i,'User Interface'])) | ('GSE01'  in (df.loc[i,'User Interface'])) | ('JMI02'  in (df.loc[i,'User Interface'])):
                        new_gb  = (df.loc[i,'Gasoil_Percent']/100) * (df.loc[i,'Factor']/100) + df.loc[i,'Oil_Loss_Correction']
                        if new_gb != df.loc[i, 'Calculation factor 1']:
                            df.loc[i,'Calculation factor 1'] = new_gb
                            df.loc[df['Formula term item number']==1, 'Start Date'] = pd.to_datetime(pd.to_datetime('today'))
                            

                else: #multiply by % for GBI etc
                    
                    # Ensure 'User Interface' column is of type string
                    # error solving
                    df['User Interface'] = df['User Interface'].astype(str)

                    if ('GBI02'  in (df.loc[i,'User Interface'])) | ('GSE01'  in (df.loc[i,'User Interface'])) | ('JMI02'  in (df.loc[i,'User Interface'])):
                        
                        new_gb  = (df.loc[i,'Gasoil_Percent']/100) * (df.loc[i,'Factor']/100) + df.loc[i,'Oil_Loss_Correction']
                        
                        if new_gb != df.loc[i, 'Calculation factor 1']:
                            df.loc[i,'Calculation factor 1'] = new_gb
                            df.loc[df['Formula term item number']==1, 'Start Date'] = pd.to_datetime('today').date()
                        
        return df
    
    def process_bio_diesel(bio_diesel):
        """
    Processes the bio_diesel DataFrame to clean and transform the data.

    This function performs the following steps:
    1. Strips whitespace from column names.
    2. Replaces 'No change' values in the 'New TP' column with the corresponding 'Current TP' values.
    3. Replaces specific substrings in the 'New TP' column.
    4. Splits the 'New TP' column into multiple rows based on the '+' delimiter.
    5. Splits the resulting 'RBDPO' column into 'Biodiesel' and 'Amount' columns.
    6. Filters the DataFrame to keep only rows where 'Biodiesel' is 'RBDPO'.
    7. Splits the 'Amount' column into 'Amount' and 'Currency' columns.
    8. Replaces 'RM/MT' with 'MYR' in the 'Currency' column.

    Parameters:
    bio_diesel (pd.DataFrame): The input DataFrame containing bio_diesel data.

    Returns:
    pd.DataFrame: A processed DataFrame containing 'Grade at Location', 'Amount', and 'Currency' columns.
    """
        bio_diesel.columns = bio_diesel.columns.str.strip()
        new_bio_diesel = bio_diesel.copy()
        new_bio_diesel.loc[new_bio_diesel['New TP'] == 'No change', 'New TP'] = new_bio_diesel['Current TP']
        new_bio_diesel['New TP'] = new_bio_diesel['New TP'].str.replace('RBDPO \+', 'RBDPO - ', regex=True).str.replace('GPC', 'GPC - ')
        new_bio_diesel['RBDPO'] = new_bio_diesel['New TP'].str.split("+")
        new_bio_diesel = new_bio_diesel.explode('RBDPO')
        new_bio_diesel[['Biodiesel', 'Amount']] = new_bio_diesel['RBDPO'].str.split("-", expand=True)
        new_bio_diesel['Biodiesel'] = new_bio_diesel['Biodiesel'].str.strip()
        
        # Filter to keep only RBDPO for gasoil
        rdb = new_bio_diesel.loc[new_bio_diesel['Biodiesel'] == 'RBDPO', ('Grade at Location', 'Amount')].copy()
        rdb[['Amount', 'Currency']] = rdb['Amount'].str.strip().str.split(" ", expand=True)
        
        rdb['Currency'] = rdb['Currency'].replace("RM/MT", "MYR")
        
        return rdb

    def for_myr(curr_df, df, sel):
        """
    Updates the surcharge values in the DataFrame based on specific conditions.

    Parameters:
    curr_df (pd.DataFrame): The reference DataFrame containing currency values.
    df (pd.DataFrame): The input DataFrame containing the data to be updated.

    Returns:
    pd.DataFrame: The updated DataFrame with modified surcharge values.
    """
        for i in range(len(df)):
            if ('MYR' in df.loc[i, 'Surcharge currency']) and (df.loc[i, 'Material_Final'] == sel) & (sel !='E5 GO 10ppm' ):
                plant = df.loc[i, 'Plant']
                value = curr_df.loc[(curr_df['Plant'] == plant) & (curr_df['Curr_Type'] == 'RM/MT'), 'Sum_Currency'].values
                
                if len(value) > 0:  # Ensure value is not empty
                    value = value[0]
                    curr_value = df.loc[i, 'Surcharge']
            
                    if isinstance(curr_value, str) and curr_value:
                        curr_value = curr_value[0]
            
                    if curr_value != value:
                        df.loc[i, 'Surcharge'] = value
                        
            elif ('MYR' in df.loc[i, 'Surcharge currency']) and (df.loc[i, 'Material_Final'] == sel) & (sel =='E5 GO 10ppm' ):
                if  ('RBDPO' not in df.loc[i-1, 'Factor_Key']) :
                    plant = df.loc[i, 'Plant']
                    try:
                        value = df.loc[ (other_curr['Plant'] == plant) & (df['Curr_Type']=='RM/MT'), 'Sum_Currency' ]
                        curr_value = df.loc[i,'Surcharge'][0]
                        if curr_value != value:
                            df.loc[i, ' Surcharge currency'] =  value 
                    except:
                        continue

        return df
    
    def for_usd(curr_df, df, sel):
        """
    Updates the 'Surcharge' column in the 'df' DataFrame for rows where the 'Surcharge currency' is 'USD' 
    Based on the 'Sum_Currency' value from the 'curr_df' DataFrame.

    Parameters:
    curr_df (pd.DataFrame): The reference DataFrame containing currency values.
    df (pd.DataFrame): The input DataFrame containing the data to be updated.

    Returns:
    None: The function modifies the 'df' DataFrame in place.
    """
        for i in range(len(df)):
            if ('USD' in df.loc[i, 'Surcharge currency']) and (df.loc[i, 'Material_Final'] == sel):
                plant = df.loc[i, 'Plant']
                value = curr_df.loc[(curr_df['Plant'] == plant) & (curr_df['Curr_Type'] == '$/bbl'), 'Sum_Currency'].values
        
                if len(value) > 0:  # Ensure value is not empty
                    value = value[0]
                    curr_value = df.loc[i, 'Surcharge']
                    
                    if isinstance(curr_value, str) and curr_value:
                        curr_value = curr_value[0]
            
                    
            
                    if curr_value != value:
                        df.loc[i, 'Surcharge'] = value
                        
        return df
    
    # the main code block 
    def final_processing(df, map_df, tp_template, depot_df1, bio_diesel, yt_one_sel):

        # initial data processing to create key in input files

        final_glued_data = process_data(df, map_df)
        # Extract the specific sheet DataFrame
        ppt_excel_org = get_sheet_df(tp_template, yt_one_sel)
        
        ppt_excel = process_ppt_excel(ppt_excel_org, yt_one_sel)
        # Read the specified sheets into a dictionary of DataFrames
        # Get list of Malayisa depots
        depot_df = depot_df1[(depot_df1['Depot_ID'].str.startswith('M')) & (~depot_df1['Depot_ID'].str.startswith('MO'))]
        
        # get plant names
        plant_df = map_depot_to_plant(depot_df)
        
        # merge depot mapping file with TP data to get plant names
        final_glued_data = final_glued_data.merge(plant_df, left_on='PlantCode', right_on='Depot_ID', how = 'left')
        final_glued_data['Plant'] = final_glued_data['Plant'].fillna("")
        final_glued_data['Plant'] = final_glued_data['Plant'].str.strip()
        
        # material mapping
        final_glued_data = map_material(final_glued_data)

        # Extend the values in the 'cols' to each line in sequence no 
        cols = ['CompanyCode', 'PlantCode','MaterialCode', 'Depot_ID','Plant','Material_Final']
        final_glued_data[cols] =  final_glued_data.groupby('Sequence No')[cols].ffill()
        final_glued_data['Calculation factor 1'] = pd.to_numeric(final_glued_data['Calculation factor 1'], errors='coerce')
        # Fill any NaN values resulting from conversion with a default value (e.g., 0)
        final_glued_data['Calculation factor 1'].fillna(0, inplace=True)

        # get oil loss correction
        # this can be obtained form the col BQ 'Calculation factor 1' of the GSAP file
        final_glued_data['Oil_Loss_Correction'] = abs(1- final_glued_data['Calculation factor 1'])

        # for gasoil we need to get the %  of gasoil blending
        if yt_one_sel == 'E5 GO 10ppm':
            final_glued_data.loc[:,'Gasoil_Percent'] = final_glued_data.loc[:,'Material Desc'].copy()
            final_glued_data['Gasoil_Percent'] = final_glued_data['Gasoil_Percent'].replace(" ","").ffill()
            final_glued_data['Gasoil_Percent'] = final_glued_data['Material Desc'].str.extract( r'(?<=B)(\d+)', expand=False)
            final_glued_data['Gasoil_Percent'].fillna(0, inplace=True)
            final_glued_data['Gasoil_Percent'] = final_glued_data['Gasoil_Percent'].ffill()
            final_glued_data['Gasoil_Percent'] = final_glued_data['Gasoil_Percent'].astype(int)

        # create key to combine dataframes
        final_glued_data['Factor_Key'] = (
        final_glued_data['Plant'].str.strip().str.replace(" ", "") +
        final_glued_data['User Interface'].str.strip().str.replace(" ", "").str.replace(r'\d+\.?\d*%', '', regex=True))
        final_glued_data['Factor_Key'] = final_glued_data['Factor_Key'].fillna("")
        
        final_glued_data = convert_column_types(final_glued_data)
        
        # get max no of lines for each sequence no
        final_glued_data = get_max_lines_per_sequence(final_glued_data)
        
       # Checks to be made
       # if no of lines are the same between excel and ppt
       # if Calculation factor is not the same, update it and update the Start Date
       # for codes like GBI multiply  % by Gasoil Percent
     
        final_glued_data = mark_last_row(final_glued_data)

       # check max no of linesin the gsap file  and no of lines in the current TP file

        final_glued_data = check_max_lines(final_glued_data)

       # subset the df only for the material for which we are making the comparison

        final_glued_data = subset_data(final_glued_data, yt_one_sel)
        
        # clear NaN values
        final_glued_data = replace_nan_values(final_glued_data, ['Surcharge currency', 'User Interface','Factor_Key'])

        # create a compare column to check common elements between the GSAP data and the excel TP input
        final_glued_data = create_compare_column(final_glued_data)
        
        # create compare column in TP excel sheet
        df_comparewith = create_compare_column_tp_excel(ppt_excel)
        
        # check for components match from ref_ppt
        final_glued_data['present_in_refppt'] = final_glued_data['compare'].isin(df_comparewith['compare']).replace({True: 'Yes', False: 'No'})

        final_glued_data['plant_in_refppt'] = final_glued_data['Plant'].isin(df_comparewith['Plant']).replace({True: 'Yes', False: 'No'}) 
        
        #check for component match from GSAP data
        df_comparewith['present_in_excel'] = df_comparewith['compare'].isin(final_glued_data['compare']).replace({True: 'Yes', False: 'No'})
        
        df_comparewith['plant_in_excel'] = df_comparewith['Plant'].isin(final_glued_data['Plant']).replace({True: 'Yes', False: 'No'})

        # drop lines
        # if plant is present in refppt but compare item is not present in ref_ppt, remove that line
        # ignore RBDPO line while dropping
        final_glued_data['mask'] = (~final_glued_data['compare'].str.contains('Last'))& (~final_glued_data['compare'].str.contains('RBDPO')) & (final_glued_data['plant_in_refppt'] == 'Yes') & (final_glued_data['present_in_refppt'] == 'Yes')
        
        # remove entries
        final_glued_data = final_glued_data.loc[ (final_glued_data['mask'] == True) | (final_glued_data['compare'].isin(['Last']) | (final_glued_data['Plant']==''))]
        # include items from refppt that are not present in GSAP data
        # get list of locations where items need to be added
        df_comparewith['mask'] = (df_comparewith['present_in_excel'] == 'No') & (df_comparewith['plant_in_excel'] == 'Yes')
        
        # create new df for items to be added
        add_df = df_comparewith.loc[df_comparewith['mask'] == True].copy()
        # remove Small Lot from add_df
        add_df = add_df.loc[~add_df['compare'].str.contains('SmallLot')]

        # Get the plants where items need to be added
        plant_list = add_df['Plant'].unique()
        # plant_list
        # subset GSAP data for the plants with ' MOPS GO 10ppm'

        temp_df = final_glued_data.loc[ (final_glued_data['Plant'].isin(plant_list)) & (final_glued_data['User Interface'].str.contains(yt_one_sel))].reset_index(drop=True).copy()
        
        temp_df['new_line_count'] = temp_df.groupby(['Sequence No'])['compare'].transform('count')

        temp_df = temp_df[temp_df['Formula term item number']==1].copy() # get only first line for reference

        # replace values from 2nd col till col 'Days for simple average' with blanks
        temp_df.loc[:, 'Cond Usage Table':'Days for simple average'] =""
        temp_df.reset_index(inplace=True,drop=True)
        
        for plt in plant_list:
            cnt = len(add_df.loc[add_df['Plant']==plt,'compare'].unique())
            # multiply entries for each sequence no by the count
            comp_list = add_df.loc[add_df['Plant']==plt,'compare'].to_list()
            for i in range(len(temp_df)):
                if temp_df.loc[i,'Plant']==plt:
                    temp_df.loc[i,'compare']= ",".join(comp_list)
                    # temp_df.loc[i,'Formula term item number'] = temp_df.loc[i,'new_line_count'] + lcnt
                
        temp_df['compare'] = temp_df['compare'].str.split(",")
        
        temp_df=temp_df.explode('compare')
        
        # Group by 'Sequence No' and forward fill with increments of 1
        temp_df['Formula term item number'] = temp_df['new_line_count'] + temp_df.groupby('Sequence No')['Formula term item number'].cumcount()+1 
        temp_df = temp_df.merge(df_comparewith[['compare','Charges']], on='compare',how='left')#.rename(columns={'Charges_x':'Charges','Charges_y':'New_Charges'})
        
        # # temp_df['Charges'] = temp_df['New_Charges']
        # # temp_df.drop('New_Charges',axis=1,inplace=True)
        temp_df['Charges']= temp_df['Charges'].str.strip()
        
        # now map temp_df with map_df and subs for quot source, type and number
        temp_df = temp_df.merge(map_df[['Quotation source','Quotation type','Quotation number','User Interface']], left_on='Charges', right_on='User Interface',how='left')#.drop('User Interface',axis=1)
        
        temp_df[['Quotation source_x','Quotation type_x', 'Quotation number_x', 'User Interface_x']] =temp_df[['Quotation source_y',
                                                                        'Quotation type_y', 'Quotation number_y', 'User Interface_y']]
        temp_df.drop(['Quotation source_y',  'Quotation type_y', 'Quotation number_y', 'User Interface_y'], axis=1, inplace=True)
        temp_df.rename(columns  = {'Quotation source_x':'Quotation source', 'Quotation type_x':'Quotation type', 'Quotation number_x':'Quotation number', 'User Interface_x':'User Interface'}, inplace=True)
        # drop columns
        temp_df.drop(['new_line_count','Charges'],axis=1,inplace=True)
        final_glued_data = pd.concat([final_glued_data, temp_df],ignore_index=True)
        
        # Custom sorting key to prioritize 'Formula term item number' = 0 at the end
        final_glued_data['Sort_Key'] = final_glued_data['Formula term item number'].apply(lambda x: 1 if x == 0 else 0)

        print("Data type error line 741")

        # Sort by 'Sequence No', 'Sort_Key', and 'Formula term item number'
        final_glued_data = final_glued_data.sort_values(['Sequence No', 'Sort_Key', 'Formula term item number'], ascending=[True, True, True])

        # Drop the temporary 'Sort_Key' column
        final_glued_data = final_glued_data.drop(columns=['Sort_Key'])
        # update factor key again
        final_glued_data['Factor_Key']= final_glued_data['Plant'].str.strip().str.replace(" ","") + final_glued_data['User Interface'].str.strip().str.replace(" ","").str.replace(r'\d+\.?\d*%', '', regex=True)

        final_glued_data['Factor_Key'] = final_glued_data['Factor_Key'].fillna("")
        ####  Merge with table for gasoil from powerpoint
        final_glued_data = final_glued_data.merge(ppt_excel[['Charges','Curr_Per',	'Curr_Type','Factor','Factor_Key', 'Lines']], on ='Factor_Key', how='left', indicator='exists')
                
        # check if no of lines is same and mark line for deletion
        final_glued_data['Lines_Diff'] = final_glued_data.apply(lambda row: 'Yes' if row['Lines'] == row['Max_Lines'] else 'No', axis = 1)
        
        # for gasoil run the RBDPO function
        if yt_one_sel == 'E5 GO 10ppm':
            rdb_1 = process_bio_diesel(bio_diesel)
            final_glued_data = update_rbdpo(final_glued_data, rdb_1)
            
        # for non-currency and non-percentage values
        final_glued_data['Quotation number'] = final_glued_data['Quotation number'].astype(str)
        final_glued_data = update_calculation_factors(final_glued_data, yt_one_sel)
        # for currency values
        other_curr = ppt_excel.loc[(ppt_excel['Curr_Per']=='Yes') & (ppt_excel['Curr_Type']!=""),['Plant','Curr_Per','Curr_Type', 'Num_Extract']]
        
        other_curr['Sum_Currency'] = other_curr.groupby(['Plant','Curr_Type'])['Num_Extract'].transform('sum')
        
        other_curr.drop_duplicates(keep='first', inplace = True)
        
        # replace NaNs in Surcharge currency column with blanks
        final_glued_data['Surcharge currency'] = final_glued_data['Surcharge currency'].fillna("")
        
        # for MYR
        final_glued_data = for_myr(other_curr, final_glued_data, yt_one_sel)

        # for USD
        final_glued_data = for_usd(other_curr, final_glued_data, yt_one_sel)

        return final_glued_data
    
    # --------------------------------------append_and_write_output------------------------
    def append_and_write_output(output_df, replaced_df, file_path):
        """
    Append the replaced_df to output_df and write the final DataFrame to a local file.

    Parameters:
    output_df (pd.DataFrame): The DataFrame to append to.
    replaced_df (pd.DataFrame): The DataFrame to append.
    file_path (str): The path to the file where the final DataFrame will be written.

    Returns:
    pd.DataFrame: The updated output DataFrame.
    """
        output_df = output_df.append(replaced_df, ignore_index=True)
        output_df.to_excel(file_path, index=False)
        return output_df
    
    # -----------------process_material-------------
    def process_materials():
        # List of materials for substitution
        yt_one = ['U95', 'U97', 'E5 GO 10ppm']
        # Initialize an empty DataFrame
        output_df = pd.DataFrame()
    
        bio_diesel = tp_template["Hydrocarbon Biodiesel B100"]
        # bio_diesel = tp_template["Hydrocarbon – Biodiesel B100"]
    
        # Process each material and concatenate the result
        for sel in yt_one:
            # replaced_df = final_processing(sel)
            replaced_df = final_processing(df, map_df, tp_template, depot_df1, bio_diesel,sel)
            output_df = pd.concat([output_df, replaced_df], ignore_index=True)

        # Save the resulting DataFrame to an Excel file
        output_df.to_excel('final_output.xlsx')
    
        # Print the DataFrame and a completion message
        return output_df
    
    final_df = process_materials()

    return final_df , tp_template

