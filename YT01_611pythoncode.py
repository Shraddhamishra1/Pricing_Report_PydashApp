import pandas as pd
import numpy as np
import io

def generate_dataframe_YT01611(GSAP_data_content, GSAP_data_filename,Material_df_611,Orbit_table_df,Customer_specific_dis):
    
    Orbit_table_df = pd.DataFrame(Orbit_table_df, index=[0])
    
    # Load GSAP_data from UI input
    if 'csv' in GSAP_data_filename:
        GSAP_data = pd.read_csv(io.StringIO(GSAP_data_content.decode('utf-8')))
    elif 'xls' in GSAP_data_filename:
        GSAP_data = pd.read_excel(io.BytesIO(GSAP_data_content))

    print(Orbit_table_df.head(2))

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
        GSAP_data.at[index, 'Material'] = apply_conditions_combined(row, index, Material_df_611, previous_results)
        previous_results[index] = GSAP_data.at[index, 'Material']
        
    GSAP_data['Concatenated'] = GSAP_data['Location'] + GSAP_data['Material']
    
    GSAP_data['Concated Data'] = GSAP_data['Location'] + GSAP_data['Material']
    
    GSAP_data = GSAP_data.merge(Customer_specific_dis[['Concated Data','Final Value']], on='Concated Data', how='left')
    
    GSAP_data = GSAP_data.merge(Orbit_table_df[['Ship-to','ULSD (cpl)','B10','B20 (cpl)']], left_on=['Formula description'], right_on=['Ship-to'], how='left').drop('Ship-to', axis=1)

    # fill TP col
    GSAP_data['TP Value'] = np.where(GSAP_data['Location']!="SFJ",pd.NA,GSAP_data['TP Value'])

    GSAP_data['TP Value'] = np.where(GSAP_data['Material']=="DIS",GSAP_data['ULSD (cpl)']-0.23,GSAP_data['TP Value'])

    GSAP_data['TP Value'] = np.where(GSAP_data['Material']=="B20",GSAP_data['B20 (cpl)']-0.23,GSAP_data['TP Value'])

    GSAP_data['TP Value'] = np.where(GSAP_data['Material']=="B10",GSAP_data['B10']-0.23,GSAP_data['TP Value'])  

    # if sequence no is blank then TP is blank
    GSAP_data['TP Value'] = np.where(GSAP_data['Sequence No'].isnull(),pd.NA,GSAP_data['TP Value'])

    return GSAP_data
 