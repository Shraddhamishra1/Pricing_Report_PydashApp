import pandas as pd
import numpy as np
import io

def generate_dataframe_YT01611(GSAP_data_content, GSAP_data_filename, mappingfile_path, Transferprice_Data_path):
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@222")
    # Load mappingfile from local path
    if 'csv' in mappingfile_path:
        mappingfile = pd.read_csv(mappingfile_path)
    elif 'xls' in mappingfile_path:
        Material_df = pd.read_excel(mappingfile_path, engine='openpyxl', dtype='object', sheet_name="611_Material")
        # TPValue_df = pd.read_excel(mappingfile_path, engine='openpyxl', dtype='object', sheet_name="611_TPValue")

    print("***********************************************8")

    # # Load TPValue_conditions from local path
    # if'csv' in mappingfile_path:
    #     TPValue_conditions = pd.read_csv(mappingfile_path)
    # elif 'xls' in mappingfile_path:
    #     TPValue_conditions = pd.read_excel(mappingfile_path, engine='openpyxl', dtype='object', sheet_name="TPValue_805")

    # Load GSAP_data from UI input
    if 'csv' in GSAP_data_filename:
        GSAP_data = pd.read_csv(io.StringIO(GSAP_data_content.decode('utf-8')))
    elif 'xls' in GSAP_data_filename:
        GSAP_data = pd.read_excel(io.BytesIO(GSAP_data_content))

    print("#################################")


    if 'csv' in Transferprice_Data_path:
        Transferprice_Data = pd.read_csv(Transferprice_Data_path)
    elif 'xls' in Transferprice_Data_path:
        # Read data from the three sheets
        Orbit_table_df = pd.read_excel(Transferprice_Data_path, engine='openpyxl', dtype='object', sheet_name="Orbit - Shipto")
        Customer_specific_dis = pd.read_excel(Transferprice_Data_path, engine='openpyxl', dtype='object', sheet_name="Customer Specific Discounts")

    print("YT01 611 FILES ARE SELECTED")
    print("*******************************########################3333333********************************")
    print('Orbit_table_df::::::::::')
    print(Orbit_table_df.head(2))
    print("*******************************########################3333333********************************")
    print('Customer_specific_dis:::::')
    print(Customer_specific_dis.head(2))
    print("*******************************########################3333333********************************")


# def process_data(file1, file2, file3):
    # GSAP_611.xlsx
    # df = pd.read_excel(file1)

    # Transfer Price Template_New1.xlsx
    # Orbit_table_df = pd.read_excel(file2, sheet_name="Orbit - Shipto")
    # Customer_specific_dis = pd.read_excel(file2, sheet_name="Customer Specific Discounts")

    # # mapping_lines_colum_trying.xlsx
    # Material_df = pd.read_excel(file3, sheet_name="611_Material")
    # TPValue_df = pd.read_excel(file3, sheet_name="611_TPValue")

    def location(x):
        if x[:3] == "FJ ":
            return "SFJ"
        else:
            return x[:3]
    
    GSAP_data['Location'] = GSAP_data['Formula description'].apply(location)
    GSAP_data['Material'] = ''
    GSAP_data['TP Value'] = ''
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

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
    
    # ---------------------------------------------------------------------------------------------
    # read the Transfer Prices sheet
    # zone_discount = pd.read_excel(tp_file, 'Transfer Prices')
    # zone_discount = zone_discount.iloc[81:93, :8]
    # zone_discount.columns = ['Key' Concated Data, 'Zone' Code, 'Material Ref' Material Code, 'Zone Description' Location , 'Discount' Location Value, 'TP' Final Value,'Unit' Uniot of Measurements,'Eff_Date'  Updated]
    
    # orbit discount table
    # Orbit_table_df = pd.read_excel(tp_file, 'Transfer Prices', header=112, usecols='B:J', nrows=57)


    # removed unnamed columns
    # Orbit_table_df = Orbit_table_df.loc[:, ~Orbit_table_df.columns.str.contains('^Unnamed')]

    # create TP column
    # concat Location and Material Ref
    # GSAP_data['Key'] = GSAP_data['Location'] + GSAP_data['Material']
    GSAP_data['Concated Data'] = GSAP_data['Location'] + GSAP_data['Material']
    
    # merge the zone_discount table
    # GSAP_data = GSAP_data.merge(Customer_specific_dis[['Key','TP']], on='Key', how='left')
    # GSAP_data = GSAP_data.merge(Customer_specific_dis[['Concated Data','Final Value']], on='Key', how='left')
    GSAP_data = GSAP_data.merge(Customer_specific_dis[['Concated Data','Final Value']], on='Concated Data', how='left')

    # merge the orbit_discount table on formula description and Ship-to
    GSAP_data = GSAP_data.merge(Orbit_table_df[['Ship-to','ULSD (cpl)','B10','B20 (cpl)']], left_on=['Formula description'], right_on=['Ship-to'], how='left').drop('Ship-to', axis=1)


    # fill TP col
    GSAP_data['TP Value'] = np.where(GSAP_data['Location']!="SFJ",pd.NA,GSAP_data['TP Value'])

    GSAP_data['TP Value'] = np.where(GSAP_data['Material']=="DIS",GSAP_data['ULSD (cpl)']-0.23,GSAP_data['TP Value'])

    GSAP_data['TP Value'] = np.where(GSAP_data['Material']=="B20",GSAP_data['B20 (cpl)']-0.23,GSAP_data['TP Value'])

    GSAP_data['TP Value'] = np.where(GSAP_data['Material']=="B10",GSAP_data['B10']-0.23,GSAP_data['TP Value'])  

    # if sequence no is blank then TP is blank
    GSAP_data['TP Value'] = np.where(GSAP_data['Sequence No'].isnull(),pd.NA,GSAP_data['TP Value'])

    # GSAP_data['Surcharge'] = GSAP_data['Surcharge'].apply(lambda x: float(x.replace("-", "")) * -1)
    # GSAP_data['Actual'] = (GSAP_data['Surcharge']) / 10
    # GSAP_data['Surcharge'] = GSAP_data['TP Value']
    # GSAP_data.drop(columns=['Location', 'Material', 'Concatenated', 'TP Value'], inplace=True)

    # Concated Data	Final Value	ULSD (cpl)	B10	B20 (cpl)


    return GSAP_data
 