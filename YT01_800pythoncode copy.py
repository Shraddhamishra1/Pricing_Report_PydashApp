import pandas as pd
import io

def generate_dataframe_YT01805(lines_conditions_content,lines_conditions_filename, tpvalue_conditions_content,tpvalue_conditions_filename,df_file_content,df_file_filename,combined_df_content,combined_df_filename):
    if 'csv' in lines_conditions_filename:
        Lines_conditions = pd.read_csv(io.StringIO(lines_conditions_content.decode('utf-8')))
    elif 'xls' in lines_conditions_filename:
        Lines_conditions = pd.read_excel(io.BytesIO(lines_conditions_content), engine='openpyxl', dtype='object', sheet_name="Lines_805")

    if 'csv' in tpvalue_conditions_filename:
        TPValue_conditions = pd.read_csv(io.StringIO(tpvalue_conditions_content.decode('utf-8')))
    elif 'xls' in tpvalue_conditions_filename:
        TPValue_conditions = pd.read_excel(io.BytesIO(tpvalue_conditions_content), engine='openpyxl', dtype='object', sheet_name="TPValue_805")

    if 'csv' in df_file_filename:
        df = pd.read_csv(io.StringIO(df_file_content.decode('utf-8')))
    elif 'xls' in df_file_filename:
        df = pd.read_excel(io.BytesIO(df_file_content))

    if 'csv' in combined_df_filename:
        combined_df = pd.read_csv(io.StringIO(combined_df_content.decode('utf-8')))    
    elif 'xls' in combined_df_filename:
        combined_df = pd.read_excel(io.BytesIO(combined_df_content))
    
    # Fill missing values
    df.fillna('', inplace=True)
    df[['Material Desc', 'Calculation factor 1', 'Varkey', 'Quotation number', 'Sequence No', 'Start Date']] = df[['Material Desc',
        'Calculation factor 1', 'Varkey', 'Quotation number', 'Sequence No', 'Start Date']].fillna(method='ffill')

    # Process Varkey and Start Date columns
    df['varkey'] = df['Varkey'].str[-9:]
    df['varkey'] = df['varkey'].replace('', '000000000')
    df['varkey'] = pd.to_numeric(df['varkey'], errors='coerce').astype(int)
    
    df['StartDateyear'] = df['Start Date'].astype(str).str[:4]
    df['StartDateyear'] = df['StartDateyear'].replace('', '00000000')
    df['StartDateyear'] = pd.to_numeric(df['StartDateyear'], errors='coerce').astype(int)
    
    df['Zone'] = ""

    def evaluate_row(row, prev_value):
        N5, I5 = row['Varkey'], row['Sequence No']
        if pd.notna(N5) and N5 != "":
            return N5[4:10] 
        elif pd.notna(I5) and I5 != "":
            return prev_value
        return prev_value

    # Function is applied row-wise and keeping track of the previous result
    prev_value = ""
    for index, row in df.iterrows():
        prev_value = evaluate_row(row, prev_value)
        df.at[index, 'Zone'] = prev_value

    df['Zone'] = df['Zone'].str.strip()

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
    df['Material'] = None

    for index, row in df.iterrows():
        result = evaluate_zone(
            row['Zone'], 
            previous_value, 
            row['Material Desc'], 
            row['Formula description'], 
            row['Surcharge currency'], 
            lookup_list
        )
        df.at[index, 'Material'] = result
        previous_value = result

    def apply_conditions_combined(row, index, conditions, previous_results, use_combined_df=False):
        # Fetch the corresponding values from combined_df based on the row's zone if needed
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
                    previous_row = df.iloc[index - 1]  # Fetch the previous row
                    # First condition for previous row and others for current row
                    if previous_row[columns_to_check[0]] == previous_results[index - 1] and all(row[columns_to_check[i]] == values[i] for i in range(1, len(columns_to_check))):
                        return result_value
                    
            elif condition_type == 'AND':
                columns_to_check = column.split(',')
                values = pattern.split(',')
                # Check if Material is the first value and len(Lines) of that row is < 1 (empty)
                if row[columns_to_check[0]] == values[0] and len(str(row[columns_to_check[1]])) < 1:
                    if use_combined_df and combined_values is not None and not combined_values.empty:
                        return combined_values[result].values[0] if result in combined_values.columns else 0
                    else:
                        return 0
                    
            elif condition_type == 'OR':
                if any(row[column] == val.strip() for val in pattern.split(',')):
                    return result_value
            
            elif condition_type == 'CountIf' and df[column].value_counts()[row[column]] > 1:
                return ""  # Assuming ERROR is the output for CountIf condition
            
        return ""

    # Call the function for Lines column
    previous_results = [""] * len(df)
    for index, row in df.iterrows():
        df.at[index, 'Lines'] = apply_conditions_combined(row, index, Lines_conditions, previous_results, use_combined_df=False)
        previous_results[index] = df.at[index, 'Lines']

    previous_results = [""] * len(df)
    for index, row in df.iterrows():
        df.at[index, 'TPValue'] = apply_conditions_combined(row, index, TPValue_conditions, previous_results, use_combined_df=True)
        previous_results[index] = df.at[index, 'TPValue']

    df['TPValue'] = df['TPValue'].replace('Zero', 0)
    df['Surcharge'] = df['TPValue']

    # Assuming df is your DataFrame
    columns_to_remove = ['Plant','Material','Extracted_Varkey','Lines','Zone','TPValue']
    df = df.drop(columns=columns_to_remove)

    return df
