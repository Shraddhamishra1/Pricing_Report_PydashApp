import numpy as np
import pandas as pd
import io

def generate_dataframe_YT04800(GSAP_data_content, GSAP_data_filename,additive_df,ref_price,jet_price,locdiff_df,plant_list):
    if 'csv' in GSAP_data_filename:
        GSAP_data = pd.read_csv(io.StringIO(GSAP_data_content.decode('utf-8')))
    elif 'xls' in GSAP_data_filename:
        GSAP_data = pd.read_excel(io.BytesIO(GSAP_data_content))
     
    ref_price.columns = ['Plant', 'Material Desc', 'TP_Ref']
    ref_price.dropna(subset=['Plant'], inplace=True)
    ref_price = ref_price.dropna(subset=['TP_Ref'])
    jet_price.columns = ['Plant', 'Jet_TP']
    locdiff_df = locdiff_df.loc[:, ~locdiff_df.columns.str.contains('^Unnamed')]
    plant_list.dropna(subset=['Plant Code'], inplace=True)

    # Process the data
    GSAP_data['Plant'] = GSAP_data.groupby('Sequence No')['Varkey'].transform(lambda x: x.str[4:8])
    GSAP_data = pd.merge(GSAP_data, plant_list, how='left', left_on='Plant', right_on='Plant Code').drop(columns=['Plant Code'])
    GSAP_data['Plant Name'] = np.where(GSAP_data['Sequence No'].isnull(), '', GSAP_data['Plant Name'])
    GSAP_data['Plant Name'] = np.where(GSAP_data['Plant Name'].isna(), 'NG', GSAP_data['Plant Name'])
    GSAP_data['Branded'] = GSAP_data['Material Desc'].apply(lambda x: 'Yes' if ('silver' in x.lower()) or ('ext' in x.lower()) or ('bronze' in x.lower()) or ('power' in x.lower()) else 'No')
    additive_df = additive_df.loc[:, ~additive_df.columns.str.contains('^Unnamed')]
    additive_df.dropna(subset=['Material Code'], inplace=True)
    additive_df['Material Code'] = additive_df['Material Code'].astype(int)
    GSAP_data['Material Number'] = GSAP_data['Varkey'].apply(lambda x: int(x[-9:]))
    GSAP_data = pd.merge(GSAP_data, additive_df, how='left', left_on='Material Number', right_on='Material Code').drop(columns=['Material Code', 'Material Name'])
    
    def material_master(row):
        if row['Branded'] == 'Yes' and pd.isna(row['Material TP Group']):
            return 'Error'
        elif row['Branded'] == 'Yes':
            return row['Material TP Group']
        elif row['Branded'] == 'No':
            return ''
        elif pd.isna(row['Seqeunce No']):
            return ''
        elif row['Sequence No'] == '':
            return ''
        else:
            return ''

    GSAP_data['Material Master Data'] = GSAP_data.apply(material_master, axis=1)

    def material(row):
        if row['Material Desc'].lower().startswith('jet'):
            return 'JET'
        elif row['Material Desc'].lower().startswith('avg'):
            return 'AVG'
        elif row['Material Desc'].lower().startswith('f-34'):
            return 'JET'
        elif row['Material Desc'][3:6].lower() == 'jet':
            return 'JET'
        elif row['Material Desc'].lower().startswith('aero'):
            return 'JET'
        elif row['Material Desc'][3:6].lower() == 'ulg':
            return 'GAS'
        elif row['Material Desc'][3:7].lower() == 'fame':
            return 'FAME'
        elif row['Material Desc'][3:7].lower() == 'etoh':
            return 'ETH'
        elif row['Material Desc'][3:7].lower() == 'hdrd':
            return 'HDRD'
        elif row['Material Desc'].lower().startswith('int'):
            return 'INT'
        elif row['Material Desc'] != '':
            return 'DIS'
        elif row['Sequence No'] == '':
            return ''
        else:
            return ''

    GSAP_data['Material'] = GSAP_data.apply(material, axis=1)
    GSAP_data = GSAP_data.merge(ref_price, how='left', left_on=['Plant', 'Material Desc'], right_on=['Plant', 'Material Desc'])
    GSAP_data = GSAP_data.merge(locdiff_df[['Plant', 'Current Gasoline (cpl)', 'Current Diesel (cpl)']], how='left', left_on='Plant', right_on='Plant')
    GSAP_data = GSAP_data.merge(jet_price, how='left', left_on='Plant', right_on='Plant')
    GSAP_data['Start Date'] = GSAP_data['Start Date'].astype(int)

    def final_tp(row):
        if int(str(row['Start Date'])[:4]) < 2021:
            return 0
        elif row['Plant'] == 'C101':
            return row['TP_Ref']
        elif row['Plant'] == 'C100':
            return row['TP_Ref']
        elif row['Material'].upper() == 'GAS':
            return row['Current Gasoline (cpl)']
        elif row['Material'].upper() == 'DIS':
            return row['Current Diesel (cpl)']
        elif row['Varkey'] in ['CA48C142000000000400004741', 'CA48C142000000000400004742', 'CA48C142000000000400011561']:
            return 0
        elif row['Material'].upper() == 'JET':
            return row['Jet_TP']
        elif row['Material Desc'][:2].upper() == 'BF':
            return 0    
        else:
            return 0
    
    GSAP_data['TP Value'] = GSAP_data.apply(final_tp, axis=1)
    GSAP_data['numval'] = GSAP_data['Value'].apply(lambda x: float(x.replace("-", "")) * (-1) if isinstance(x, str) and x[-1] == '-' else x)
    GSAP_data['numval'] = GSAP_data['numval'].apply(lambda x: round(float(x) / 10, 2))
    GSAP_data['tp_diff'] = GSAP_data['TP Value'] - GSAP_data['numval']
    GSAP_data['Cond_Usage_Table'] = GSAP_data.apply(lambda row: "" if row['TP Value'] == 0 else ("" if row['tp_diff'] == 0 else False), axis=1)
    GSAP_data['Cond_Usage_Table'] = GSAP_data.groupby('Sequence No')['Cond_Usage_Table'].transform('ffill')
    GSAP_data['Value'] = GSAP_data['TP Value']

    return GSAP_data