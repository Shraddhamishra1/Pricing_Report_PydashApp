import pandas as pd
import io

def generate_dataframe_EthanolCBOB(Ethanol_Gsapdata_content, Ethanol_Gsapdata_filename,ZonalTP):

    if 'csv' in Ethanol_Gsapdata_filename:
        Ethanol_Gsapdata = pd.read_csv(io.StringIO(Ethanol_Gsapdata_content.decode('utf-8')))
    elif 'xls' in Ethanol_Gsapdata_filename:
        Ethanol_Gsapdata = pd.read_excel(io.BytesIO(Ethanol_Gsapdata_content))

    def calculate_value(calculation_factor1, varkey, ZonalTP):
        if calculation_factor1 == 1 or calculation_factor1 == 1.1111:
            if varkey[-9:] == "400004678" or varkey[-9:] == "400004679":
                
                lookup_value = varkey[4:9]
                result = ZonalTP[ZonalTP['Zone'] == lookup_value]['Ethanol (USCPG)']
                if not result.empty:
                    return result.values[0]
            else:
                lookup_value = varkey[4:9]
                result = ZonalTP[ZonalTP['Zone'] == lookup_value]['Regular Gasoline (cpl)'] * 10
                if not result.empty:
                    return result.values[0]
        else:
            lookup_value = varkey[4:9]
            result = ZonalTP[ZonalTP['Zone'] == lookup_value]['Ethanol (USCPG)']
            if not result.empty:
                return result.values[0]
        
        return None  # Return None if no match is found

    # Convert the 'Varkey' column to strings outside the loop
    Ethanol_Gsapdata['Varkey'] = Ethanol_Gsapdata['Varkey'].ffill()
    Ethanol_Gsapdata['Varkey'] = Ethanol_Gsapdata['Varkey'].astype(str)

    # Apply the function to your existing DataFrame
    Ethanol_Gsapdata['TPValue'] = Ethanol_Gsapdata.apply(lambda row: calculate_value(row['Calculation factor 1'], row['Varkey'], ZonalTP), axis=1)

    Ethanol_Gsapdata['Surcharge'] = Ethanol_Gsapdata['TPValue']
    Ethanol_Gsapdata.drop(columns=['TPValue'], inplace=True)

    return Ethanol_Gsapdata

