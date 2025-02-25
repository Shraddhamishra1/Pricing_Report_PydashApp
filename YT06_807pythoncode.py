import pandas as pd
import io

def generate_dataframe_YT06807(YT06_807_GsapData_content, YT06_807_GsapData_filename,Additive_MaterialCode,Additive_TPcost):

    if 'csv' in YT06_807_GsapData_filename:
        YT06_807_GsapData = pd.read_csv(io.StringIO(YT06_807_GsapData_content.decode('utf-8')))
    elif 'xls' in YT06_807_GsapData_filename:
        YT06_807_GsapData = pd.read_excel(io.BytesIO(YT06_807_GsapData_content))

    YT06_807_GsapData['GSAP_MaterialNumber'] = YT06_807_GsapData['Varkey'].apply(lambda x: int(x[-9:]))

    # Merge with Additive_MaterialCode
    YT06_807_GsapData = pd.merge(YT06_807_GsapData, Additive_MaterialCode, left_on='GSAP_MaterialNumber', right_on='Material Code', how='left')
    YT06_807_GsapData.drop(columns=['Material Name', 'Material Code'], inplace=True)

    # Merge with Additive_TPcost
    YT06_807_GsapData = pd.merge(YT06_807_GsapData, Additive_TPcost, on='Material TP Group', how='left')

    # Calculate Surcharge
    YT06_807_GsapData['Surcharge'] = YT06_807_GsapData.apply(lambda row: row['ADDITIVE COST ( $ / L )'] * 1000 if pd.notnull(row['GSAP_MaterialNumber']) else "", axis=1)
    YT06_807_GsapData['Value'] = YT06_807_GsapData['Surcharge']
    YT06_807_GsapData.drop(columns=['GSAP_MaterialNumber', 'Material TP Group', 'ADDITIVE COST ( $ / L )', 'Surcharge'], inplace=True)

    return YT06_807_GsapData

