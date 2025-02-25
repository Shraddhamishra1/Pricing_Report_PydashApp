import pandas as pd
import numpy as np
import io

def generate_dataframe_YT01800(GSAP_data_content, GSAP_data_filename,Lines_conditions,TPValue_conditions_800, Zonal_TP,Biofuels_prices,AviationT_prices,CF_CN_Locomotive_Discount,B20_Discount_by_Plant,Zone_Plant_mapping):
    # Load GSAP_data from UI input
    if 'csv' in GSAP_data_filename:
        GSAP_data = pd.read_csv(io.StringIO(GSAP_data_content.decode('utf-8')))
    elif 'xls' in GSAP_data_filename:
        GSAP_data = pd.read_excel(io.BytesIO(GSAP_data_content))

    # Combine dataframes
    combined_df = Zonal_TP.merge(Biofuels_prices, on='Zone').merge(AviationT_prices, on='Zone')
    combined_df.rename(columns={'Jet (cpl)_x': 'Jet (cpl)', 'Location_x':'Location'}, inplace=True)
    
    columns_to_keep = ['Zone', 'Location', 'Regular Gasoline (cpl)', 'Midgrade Gasoline (cpl)', 'Premium Gasoline (cpl)',
                   'Premium 93 Gasoline (cpl)', 'Furnace (cpl)', 'Stove (cpl)', 'ULSD (cpl)', 'Loco Diesel (cpl)', 'Jet (cpl)',
                   'Ethanol (USCPG)', 'Updated', 'Bio Fuel Pricing', 'HDRD (USD/100 GAL)', 'FAME (USD/100 GAL)', 'Avgas',
                   'Avgas Volume (cpl)', 'Notes']

    combined_df = combined_df[columns_to_keep]

    grouped = Zone_Plant_mapping.groupby('Zone')['GSAP Plant'].unique().reset_index()
    grouped['GSAP Plant'] = grouped['GSAP Plant'].apply(list)

    # Define the custom function
    def get_value(varkey, sequence_no, prev_result):
        if pd.notna(varkey) and varkey.strip() != "":
            return varkey[4:8]
        elif pd.notna(sequence_no):
            return prev_result
        return ""
    
    # Initialize the 'Plant' column with empty strings
    GSAP_data['Plant'] = ""
    
    # Iterate through rows using index-based iteration
    for i in range(len(GSAP_data)):
        prev_result = GSAP_data.loc[i - 1, 'Plant'] if i > 0 else ""
        GSAP_data.at[i, 'Plant'] = get_value(GSAP_data.loc[i, 'Varkey'], GSAP_data.loc[i, 'Sequence No'], prev_result)

    # Define keywords for conditions
    chem_keywords = ['REF', 'LUB', 'INT ', 'MFO ', 'US ', 'MGO ', 'VGO', 'DEC', 'SUL', 'HFO', 'SB ']
    dis_keywords = ['IGO ', 'AGO ', 'ULSD ']
    
    GSAP_data[['Cond Usage Table', 'Formula description', 'Material Desc']] = GSAP_data[['Cond Usage Table', 'Formula description', 'Material Desc']].fillna(method='ffill')
    
    # Apply the conditions in one line
    GSAP_data['Material'] = GSAP_data.apply(lambda row: (
        '' if pd.isna(row['Sequence No']) else
        '' if pd.isna(row['Cond Usage Table']) else
        'CHEM' if any(keyword in str(row['Formula description']) or keyword in str(row['Material Desc']) for keyword in chem_keywords) else
        'ETH' if 'ETHANOL' in str(row['Formula description']) else
        'JET' if 'Jet ' in str(row['Material Desc']) else
        'GAS' if 'ULG ' in str(row['Material Desc']) else
        'LOCO' if 'Loco ' in str(row['Material Desc']) else
        'DIS' if any(keyword in str(row['Material Desc']) for keyword in dis_keywords) else
        str(row['Material Desc'])[3:6] if 'BF ' in str(row['Material Desc']) else
        str(row['Formula description'])[:3] if pd.notna(row['Sequence No']) else
        ''
    ), axis=1)

    GSAP_data['Varkey'] = GSAP_data['Varkey'].replace('', '00000000000000000000000000')
    GSAP_data['Extracted_Varkey'] = GSAP_data['Varkey'].str.strip().str[-9:].fillna('00000000')
    GSAP_data['Extracted_Varkey'] = GSAP_data['Extracted_Varkey'].astype(int)
    GSAP_data['Lines'] = np.nan
    GSAP_data['Start Date'] = GSAP_data['Start Date'].astype(str)

    def apply_conditions_combined(row, index, conditions, previous_results, use_combined_df=False):
        if use_combined_df and 'Zone' in row and 'Plant' in row:
            combined_values = combined_df[(combined_df['Zone'] == row['Zone']) & (combined_df['Plant'] == row['Plant'])]
        else:
            combined_values = None
        
        for _, condition in conditions.iterrows():
            column = condition['Column to Check']
            condition_type = condition['Condition Type']
            pattern = condition['Condition Pattern/Value']
            result = condition['Result']
            
            if use_combined_df and combined_values is not None and not combined_values.empty:
                result_value = combined_values[result].values[0]
            else:
                result_value = result
            
            if condition_type == 'Contains' and pattern in str(row[column]):
                return result_value
            
            elif condition_type == 'Equals' and row[column] == pattern:
                return result_value
            elif condition_type == 'EndsWith' and str(row[column]).endswith(pattern):
                return result_value
            elif condition_type == 'StartsWith' and str(row[column]).startswith(pattern):
                return result_value
            elif pd.isna(pattern) or pattern == '':
                if condition_type == 'ISBLANK' and pd.isna(row[column]):
                    return result_value
            elif condition_type == 'ISBLANK' and pd.isna(row[column]):
                return 0
            elif condition_type == 'NUMBERVALUE':
                operator = pattern.split(' ')[1]
                pattern_year = int(pattern.split(operator)[1].strip())
                if eval(f"{row[column]} {operator} {pattern_year}"):
                    return result_value
            elif condition_type == 'GreaterThan' and row[column] > float(pattern):
                return result_value
            elif condition_type == 'LessThan' and row[column] < float(pattern):
                return result_value
            elif condition_type == 'And':
                columns_to_check = column.split(',')
                values = pattern.split(',')

                if index > 0:
                    previous_row = GSAP_data.iloc[index - 1]
                    if previous_row[columns_to_check[0]] == previous_results[index - 1] and all(row[columns_to_check[i]] == values[i] for i in range(1, len(columns_to_check))):
                        return result_value
                    
            elif condition_type == 'AND':
                columns_to_check = column.split(',')
                values = pattern.split(',')

                # Check if all conditions are met
                conditions_met = all(row[columns_to_check[i]] == values[i] for i in range(len(columns_to_check)))
                if conditions_met:
                    if use_combined_df and combined_values is not None and not combined_values.empty:
                        return combined_values[result].values[0] * 10 if result in combined_values.columns else 0
                    else:
                        return 0
                                
            elif condition_type == 'OR' and any(row[column] == val.strip() for val in pattern.split(',')):
                return result_value
            elif condition_type == 'CountIf' and GSAP_data[column].value_counts()[row[column]] > 1:
                return ""
        return ""

    previous_results = [""] * len(GSAP_data)
    for index, row in GSAP_data.iterrows():
        GSAP_data.at[index, 'Result'] = apply_conditions_combined(row, index, Lines_conditions, previous_results, use_combined_df=False)
        previous_results[index] = GSAP_data.at[index, 'Result']

    GSAP_data['Lines'] = GSAP_data['Result']
    
    combined_merged_withplants = pd.merge(grouped, combined_df, on='Zone', how='left')
    combined_df = combined_merged_withplants.explode('GSAP Plant')
    combined_df = combined_df.rename(columns={'GSAP Plant': 'Plant'})
    combined_df['Zero'] = 0
    combined_df['Three'] = 3
    
    exploded_grouped = grouped.explode('GSAP Plant')
    exploded_grouped = exploded_grouped.rename(columns={'GSAP Plant': 'Plant'})
    GSAP_data = pd.merge(GSAP_data, exploded_grouped, on='Plant', how='left')
    
    B20_Discount_by_Plant = B20_Discount_by_Plant.rename(columns={'Plants': 'Plant'}).fillna(0).head(4)
    B20_Discount_by_Plant = B20_Discount_by_Plant.loc[:, ~B20_Discount_by_Plant.columns.duplicated()]
    B20_Discount_by_Plant = B20_Discount_by_Plant[['Plant', 'Total YT01 805/Discount']]

    CF_CN_Locomotive_Discount = CF_CN_Locomotive_Discount.rename(columns={'Plant ': 'Plant', 'Uploaded Discount ': 'Uploaded Discount'}).fillna(0)
    CF_CN_Locomotive_Discount = CF_CN_Locomotive_Discount[['Plant', 'Uploaded Discount']]

    combined_df = combined_df.merge(B20_Discount_by_Plant, on='Plant', how='left').merge(CF_CN_Locomotive_Discount, on='Plant', how='left')
    
    previous_results = [""] * len(GSAP_data)
    for index, row in GSAP_data.iterrows():
        GSAP_data.at[index, 'TPValue'] = apply_conditions_combined(row, index, TPValue_conditions_800, previous_results, use_combined_df=True)
        previous_results[index] = GSAP_data.at[index, 'TPValue']
    
    GSAP_data['TPValue'] = GSAP_data['TPValue'].replace('Zero', 0)
    GSAP_data['TPValue'] = GSAP_data['TPValue'].replace('Three', 3)
    
    return GSAP_data