import pandas as pd
import io

def generate_dataframe_YT01805(GSAP_data_content, GSAP_data_filename,mappingfile,TPValue_conditions_805,zonal_tp,bio_fuels,aviation_fuel):

    if 'csv' in GSAP_data_filename:
        GSAP_data = pd.read_csv(io.StringIO(GSAP_data_content.decode('utf-8')))
    elif 'xls' in GSAP_data_filename:
        GSAP_data = pd.read_excel(io.BytesIO(GSAP_data_content))
    
    combined_df = zonal_tp.merge(bio_fuels, on='Zone', how='outer') \
                      .merge(aviation_fuel, on='Zone', how='outer') \
                      [['Location_x', 'Zone', 'Regular Gasoline (cpl)', 'Midgrade Gasoline (cpl)', 
                        'Premium Gasoline (cpl)', 'Premium 93 Gasoline (cpl)', 'Furnace (cpl)', 'Stove (cpl)', 
                        'ULSD (cpl)', 'Loco Diesel (cpl)', 'Jet (cpl)_x', 'Ethanol (USCPG)', 'Updated', 'HDRD (USD/100 GAL)',
                          'FAME (USD/100 GAL)', 'Avgas']]
    
    combined_df.columns = ['Location', 'Zone', 'Regular Gasoline (cpl)', 'Midgrade Gasoline (cpl)',
                            'Premium Gasoline (cpl)', 'Premium 93 Gasoline (cpl)', 'Furnace (cpl)', 'Stove (cpl)', 
                            'ULSD (cpl)', 'Loco Diesel (cpl)', 'Jet (cpl)', 'Ethanol (USCPG)', 'Updated', 'HDRD (USD/100 GAL)', 
                            'FAME (USD/100 GAL)', 'Avgas']
    
    # Add a new 'Zero' column with all values set to 0
    combined_df['Zero'] = 0

    # Fill missing values
    GSAP_data.fillna('', inplace=True)
    GSAP_data[['Material Desc', 'Calculation factor 1', 'Varkey', 'Quotation number', 'Sequence No', 'Start Date']] = GSAP_data[['Material Desc',
        'Calculation factor 1', 'Varkey', 'Quotation number', 'Sequence No', 'Start Date']].fillna(method='ffill')
    
    # Process Varkey and Start Date columns
    GSAP_data['varkey'] = GSAP_data['Varkey'].str[-9:]
    GSAP_data['varkey'] = GSAP_data['varkey'].replace('', '000000000')
    GSAP_data['varkey'] = pd.to_numeric(GSAP_data['varkey'], errors='coerce').astype(int)
    GSAP_data['StartDateyear'] = GSAP_data['Start Date'].astype(str).str[:4]
    GSAP_data['StartDateyear'] = GSAP_data['StartDateyear'].replace('', '00000000')
    GSAP_data['StartDateyear'] = pd.to_numeric(GSAP_data['StartDateyear'], errors='coerce').astype(int)
    GSAP_data['Zone'] = ""

    def evaluate_row(row, prev_value):
        N5, I5 = row['Varkey'], row['Sequence No']
        if pd.notna(N5) and N5 != "":
            return N5[4:10] 
        elif pd.notna(I5) and I5 != "":
            return prev_value
        return prev_value

    # Function is applied row-wise and keeping track of the previous result
    prev_value = ""
    for index, row in GSAP_data.iterrows():
        prev_value = evaluate_row(row, prev_value)
        GSAP_data.at[index, 'Zone'] = prev_value

    GSAP_data['Zone'] = GSAP_data['Zone'].str.strip()
    lookup_list = ["DIS", "KER", "MGO", "FUR"]

    def evaluate_zone(zone, previous_value, material_desc, formula_desc, surcharge_currency, lookup_list):
        if zone[:3] == "CAZ":
            if not material_desc:
                return previous_value
            if formula_desc[:3] == "ETH":
                return "ETH"
            if material_desc[:3] == "KER":
                return "KER"
            if material_desc[:3] == "AVG":
                return "AVG"
            if material_desc[:3] == "INT":
                return "INT"
            if surcharge_currency == "USD":
                return "N/A"
            if formula_desc[:3] in lookup_list:
                return "DIS"
            return formula_desc[:3]
        return None

    previous_value = "prev_val"
    GSAP_data['Material'] = None

    for index, row in GSAP_data.iterrows():
        result = evaluate_zone(
            row['Zone'], 
            previous_value, 
            row['Material Desc'], 
            row['Formula description'], 
            row['Surcharge currency'], 
            lookup_list
        )
        GSAP_data.at[index, 'Material'] = result
        previous_value = result

    def apply_conditions_combined(row, index, conditions, previous_results, use_combined_df=False):
        # Fetch the corresponding values from Transferprice_Data based on the row's zone if needed
        if use_combined_df and 'Zone' in row and row['Zone'] in combined_df['Zone'].values:
            combined_values = combined_df.loc[combined_df['Zone'] == row['Zone']]
        else:
            combined_values = None

        for _, condition in conditions.iterrows():
            column = condition['Column to Check']
            condition_type = condition['Condition Type']
            pattern = condition['Condition Pattern/Value']
            result = condition['Result']  

            # Determine the result value based on the presence of combined_values
            if use_combined_df and combined_values is not None and not combined_values.empty:
                result_value = combined_values[result].values[0]
            else:
                result_value = result

            # Apply condition based on the type
            if condition_type == 'Contains' and pattern in str(row[column]):
                return result_value
            
            elif condition_type == 'Equals' and row[column] == pattern:
                return result_value
            
            elif condition_type == 'EndsWith' and str(row[column]).endswith(pattern):
                return result_value
            
            elif condition_type == 'StartsWith' and str(row[column]).startswith(pattern):
                return result_value
            
            elif pd.isna(pattern) or pattern == '':
                # Handle specific types for blanks
                if condition_type == 'ISBLANK':
                    if pd.isna(row[column]):
                        return result_value

            elif condition_type == 'ISBLANK' and pd.isna(row[column]):
                return 0  # Assuming 0 for ISBLANK condition

            elif condition_type == 'NUMBERVALUE':
                operator = pattern.split(' ')[1]
                pattern_year = int(pattern.split(operator)[1].strip())
                if eval(f"{row[column]} {operator} {pattern_year}"):
                    return result_value

            elif condition_type == 'GreaterThan':
                if row[column] > float(pattern):
                    return result_value

            elif condition_type == 'LessThan':
                if row[column] < float(pattern):
                    return result_value

            elif condition_type == 'And':
                columns_to_check = column.split(',')
                values = pattern.split(',')
                if index > 0:  # Check if current index is greater than 0
                    previous_row = GSAP_data.iloc[index - 1]  # Fetch the previous row
                    # First condition for previous row and others for current row
                    if previous_row[columns_to_check[0]] == previous_results[index - 1] and all(row[columns_to_check[i]] == values[i] for i in range(1, len(columns_to_check))):
                        return result_value
                    
            elif condition_type == 'AND':
                columns_to_check = column.split(',')
                values = pattern.split(',')
                # Check if Material is the first value and len(Lines) of that row is < 1 (empty)
                if row[columns_to_check[0]] == values[0] and len(str(row[columns_to_check[1]])) < 1:
                    if use_combined_df and combined_values is not None and not combined_values.empty:
                        return combined_values[result].values[0] * 10 if result in combined_values.columns else 0
                    else:
                        return 0
                    
            elif condition_type == 'OR':
                if any(row[column] == val.strip() for val in pattern.split(',')):
                    return result_value
            
            elif condition_type == 'CountIf' and GSAP_data[column].value_counts()[row[column]] > 1:
                return ""  # Assuming ERROR is the output for CountIf condition
            
        return ""

    # Call the function for Lines column
    previous_results = [""] * len(GSAP_data)
    for index, row in GSAP_data.iterrows():
        GSAP_data.at[index, 'Result'] = apply_conditions_combined(row, index, mappingfile, previous_results, use_combined_df=False)
        previous_results[index] = GSAP_data.at[index, 'Result']

    GSAP_data['Lines'] = GSAP_data['Result']

    previous_results = [""] * len(GSAP_data)
    for index, row in GSAP_data.iterrows():
        GSAP_data.at[index, 'TPValue'] = apply_conditions_combined(row, index, TPValue_conditions_805, previous_results, use_combined_df=True)
        previous_results[index] = GSAP_data.at[index, 'TPValue']

    GSAP_data['TPValue'] = GSAP_data['TPValue'].replace('Zero', 0)
    GSAP_data['Surcharge'] = GSAP_data['TPValue']

    # Assuming GSAP_data is your DataFrame
    columns_to_remove = ['varkey','StartDateyear','Zone','Material','Result','Lines','TPValue']
    GSAP_data = GSAP_data.drop(columns=columns_to_remove)

    return GSAP_data