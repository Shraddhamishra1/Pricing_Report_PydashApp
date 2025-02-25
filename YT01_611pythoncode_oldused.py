import pandas as pd
import numpy as np
import io

def generate_dataframe_YT01611(GSAP_data_content, GSAP_data_filename, mappingfile_path, Transferprice_Data_path):
    # Load mappingfile from local path
    print(mappingfile_path)
    if 'csv' in mappingfile_path:
        mappingfile = pd.read_csv(mappingfile_path)
    elif 'xls' in mappingfile_path:
        Material_df = pd.read_excel(mappingfile_path, engine='openpyxl', dtype='object', sheet_name="611_Material")
        TPValue_df = pd.read_excel(mappingfile_path, engine='openpyxl', dtype='object', sheet_name="611_TPValue")

    # Load GSAP_data from UI input
    if 'csv' in GSAP_data_filename:
        GSAP_data = pd.read_csv(io.StringIO(GSAP_data_content.decode('utf-8')))
    elif 'xls' in GSAP_data_filename:
        GSAP_data = pd.read_excel(io.BytesIO(GSAP_data_content))

    if 'csv' in Transferprice_Data_path:
        Transferprice = pd.read_csv(Transferprice_Data_path)
    elif 'xls' in Transferprice_Data_path:
        print(Transferprice_Data_path)
        Orbit_table_df = pd.read_excel(Transferprice_Data_path, engine='openpyxl', dtype='object', sheet_name='Orbit - Shipto')
        Customer_specific_dis = pd.read_excel(Transferprice_Data_path, engine='openpyxl', dtype='object', sheet_name='Customer Specific Discounts')
     
    def location(x):
        if x[:3] == "FJ ":
            return "SFJ"
        else:
            return x[:3]
    
    GSAP_data['Location'] = GSAP_data['Formula description'].apply(location)
    GSAP_data['Material'] = ''
    GSAP_data['TP Value'] = ''

    def apply_conditions_combined(row, index, conditions, previous_results):
        for _, condition in conditions.iterrows():
            column = condition['Column to Check']
            condition_type = condition['Condition Type']
            pattern = condition['Condition Pattern/Value']
            result = condition['Result']  

            # Apply condition based on the type
            if condition_type == 'Contains' and pattern in str(row[column]):
                return result
            
            elif pd.isna(pattern) or pattern == '':
                # Handle specific types for blanks
                if condition_type == 'ISBLANK':
                    if pd.isna(row[column]):
                        return result

            elif condition_type == 'ISBLANK' and pd.isna(row[column]):
                return 0  # Assuming 0 for ISBLANK condition

            elif condition_type == "CheckNotBlank" and not pd.isnull(row[column]):
                return result
            
        return ""

    # Call the function for Lines column
    previous_results = [""] * len(GSAP_data)
    for index, row in GSAP_data.iterrows():
        GSAP_data.at[index, 'Material'] = apply_conditions_combined(row, index, Material_df, previous_results)
        previous_results[index] = GSAP_data.at[index, 'Material']

    GSAP_data['Concatenated'] = GSAP_data['Location'] + GSAP_data['Material']

    def apply_conditions_to_df(GSAP_data, condition_table, Orbit_table_df , Customer_specific_dis ,result_column):
        """
        Apply conditions from the condition_table to the GSAP_data dataframe and update the result_column.
        
        Parameters:
        GSAP_data (pd.DataFrame): The main DataFrame where conditions will be applied.
        condition_table (pd.DataFrame): Table containing Python Equivalent conditions and result logic.
        result_column (str): Column name in GSAP_data where the result will be written.
        
        Returns:
        pd.DataFrame: The modified DataFrame with the updated result_column.
        """
        for index, row in GSAP_data.iterrows():
            for _, condition_row in condition_table.iterrows():
                condition = condition_row['Python Equivalent']  
                result_value = condition_row['Result']
                
                # Evaluate the condition and store the result if it's true
                if eval(condition):
                    # Assign result_value or evaluated value to the respective column
                    GSAP_data.at[index, result_column] = eval(result_value) if result_column == 'TP Value' else result_value
                    
                    break  # Exit the inner loop once the condition is true
        return GSAP_data

    GSAP_data = apply_conditions_to_df(GSAP_data, TPValue_df,Orbit_table_df , Customer_specific_dis ,  'TP Value')

    GSAP_data['Surcharge'] = GSAP_data['Surcharge'].apply(lambda x: float(x.replace("-", "")) * -1)
    GSAP_data['Actual'] = (GSAP_data['Surcharge']) / 10
    GSAP_data['Check'] = np.where(GSAP_data['TP Value'] ==  GSAP_data['Actual'], '', 'FALSE')
    GSAP_data['Surcharge'] = GSAP_data['TP Value']
    GSAP_data.drop(columns=['Location', 'Material', 'Concatenated', 'Actual', 'Check','TP Value'], inplace=True)

    return GSAP_data