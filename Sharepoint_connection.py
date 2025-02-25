import os
import requests
from dotenv import load_dotenv
import pandas as pd
from io import BytesIO

def get_access_token(tenant_id, client_id, client_secret):
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    body = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }
    response = requests.post(url, data=body)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print('Error getting access token:', response.status_code, response.text)
        return None

def get_site_id(access_token, sharepoint_root, site_url):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f'https://graph.microsoft.com/v1.0/sites/{sharepoint_root}:{site_url}', headers=headers)
    if response.status_code == 200:
        return response.json().get('id')
    else:
        print('Error getting site ID:', response.status_code, response.text)
        return None

def get_drive_id(access_token, site_id, library):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives', headers=headers)
    if response.status_code == 200:
        drives = response.json().get('value', [])
        drive = next((d for d in drives if d['name'] == library), None)
        if drive:
            return drive['id']
        else:
            print(f"Library '{library}' not found.")
            return None
    else:
        print('Error getting drives:', response.status_code, response.text)
        return None

def get_folder_id(access_token, site_id, drive_id, folders):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root/children"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json().get('value', [])
        for folder_name in folders.split('/'):
            folder = next((item for item in response_json if item['name'] == folder_name), None)
            if folder:
                folder_id = folder['id']
                url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/items/{folder_id}/children"
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    response_json = response.json().get('value', [])
                else:
                    print("Error fetching children:", response.status_code, response.text)
                    return None
            else:
                print(f"Folder '{folder_name}' not found.")
                return None
        return response_json
    else:
        print("Error fetching root children:", response.status_code, response.text)
        return None

def download_file(access_token, site_id, drive_id, file_id):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    download_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/items/{file_id}/content"
    file_response = requests.get(download_url, headers=headers)
    if file_response.status_code == 200:
        return file_response.content
    else:
        print("Error downloading file:", file_response.status_code, file_response.text)
        return None

def load_files_from_SP():
# def main():
    load_dotenv()

    ca_tenant_id = os.getenv('ca_tenant_id')
    ca_client_id = os.getenv('ca_client_id')
    ca_client_secret = os.getenv('ca_client_secret')
    ca_sharepoint_root = os.getenv('ca_sharepoint_root')
    ca_site_url = os.getenv('ca_site_url')
    ca_library = os.getenv('ca_library')
    ca_folders = os.getenv('ca_folders')

    access_token = get_access_token(ca_tenant_id, ca_client_id, ca_client_secret)
    if not access_token:
        return

    site_id = get_site_id(access_token, ca_sharepoint_root, ca_site_url)
    if not site_id:
        return

    drive_id = get_drive_id(access_token, site_id, ca_library)
    if not drive_id:
        return

    folder_contents = get_folder_id(access_token, site_id, drive_id, ca_folders)
    if not folder_contents:
        return
    
    files_to_download = ['mapping_conditionsfile.xlsx', 'Transfer Price Template_New1.xlsx']

    for file_name in files_to_download:
        file = next((item for item in folder_contents if 'file' in item and item['name'] == file_name), None)
        if file:
            file_content = download_file(access_token, site_id, drive_id, file['id'])
            if file_content:
                if file_name == 'mapping_conditionsfile.xlsx':
                    print(f"Downloaded {file_name}")
                    
                    # reports used for 805 report
                    mappingfile = pd.read_excel(BytesIO(file_content), sheet_name="Lines_805")
                    TPValue_conditions_805 = pd.read_excel(BytesIO(file_content), sheet_name="TPValue_805")

                    # reports used for 800 report
                    Lines_conditions = pd.read_excel(BytesIO(file_content), sheet_name="Lines_800_automate")
                    TPValue_conditions_800 = pd.read_excel(BytesIO(file_content), sheet_name="800_TPValue_automate")

                    # reports used for 611 report
                    Material_df_611 = pd.read_excel(BytesIO(file_content), sheet_name="611_Material")

                elif file_name == 'Transfer Price Template_New1.xlsx':
                    print(f"Downloaded {file_name}")

                    Transferprice_Historical_CA = pd.read_excel(BytesIO(file_content), engine='openpyxl', dtype='object', sheet_name=None)
                    Orbit_table_df = pd.read_excel(BytesIO(file_content), sheet_name="Orbit - Shipto")
                    Customer_specific_dis = pd.read_excel(BytesIO(file_content), sheet_name="Customer Specific Discounts")

                    # reports used for YT01 805 report
                    zonal_tp = pd.read_excel(BytesIO(file_content), sheet_name='Zonal TP')
                    bio_fuels = pd.read_excel(BytesIO(file_content), sheet_name='Bio Fuels')
                    aviation_fuel = pd.read_excel(BytesIO(file_content), sheet_name='Aviation Fuel')

                    # reports used for YT01 800 report
                    Zonal_TP = pd.read_excel(BytesIO(file_content), sheet_name='Zonal TP')
                    Biofuels_prices = pd.read_excel(BytesIO(file_content), sheet_name='Bio Fuels')
                    AviationT_prices = pd.read_excel(BytesIO(file_content), sheet_name='Aviation Fuel')
                    CF_CN_Locomotive_Discount = pd.read_excel(BytesIO(file_content), sheet_name='Locomotive Discounts')
                    B20_Discount_by_Plant = pd.read_excel(BytesIO(file_content), sheet_name='B20 Discount by Plant')
                    Zone_Plant_mapping = pd.read_excel(BytesIO(file_content), sheet_name='GSAP Plant and Codes')

                    # reports used for YT04 800 report
                    additive_df = pd.read_excel(BytesIO(file_content), sheet_name='Material_Code')
                    ref_price = pd.read_excel(BytesIO(file_content), sheet_name='Lists', usecols='S:U', skiprows=1)
                    jet_price = pd.read_excel(BytesIO(file_content),sheet_name='Lists', usecols='W:X', skiprows=1, nrows=58)
                    locdiff_df = pd.read_excel(BytesIO(file_content), sheet_name='Location Differences')
                    plant_list = pd.read_excel(BytesIO(file_content), sheet_name='Lists')

                    # reports used for YT06 807 report
                    Additive_MaterialCode = pd.read_excel(BytesIO(file_content), sheet_name='Material_Code')
                    Additive_TPcost = pd.read_excel(BytesIO(file_content),sheet_name='YT06_807_Additives_Rate',skiprows=14,header=1)

                    # reports used for Ethanol report
                    ZonalTP = pd.read_excel(BytesIO(file_content), sheet_name='Zonal TP')

                    # reports used for Ottawa report
                    Ottawa_kgsBlv_TP = pd.read_excel(BytesIO(file_content), sheet_name='Otta, Kings and Bellev')                    

        else:
            print(f"File '{file_name}' not found.")

    print('Successfully loaded files from Sharepoint')
    print("***************************************")

    return mappingfile,TPValue_conditions_805,zonal_tp,bio_fuels,aviation_fuel,Lines_conditions,TPValue_conditions_800, Zonal_TP,Biofuels_prices,AviationT_prices,CF_CN_Locomotive_Discount,B20_Discount_by_Plant,Zone_Plant_mapping,Material_df_611,Orbit_table_df,Customer_specific_dis, additive_df,ref_price,jet_price,locdiff_df,plant_list,Additive_MaterialCode,Additive_TPcost,ZonalTP,Ottawa_kgsBlv_TP,Transferprice_Historical_CA

def load_files_from_SP_MY():
    load_dotenv()

    gscf_tenant_id = os.getenv('gscf_tenant_id')
    gscf_client_id = os.getenv('gscf_client_id')
    gscf_client_secret = os.getenv('gscf_client_secret')
    gscf_sharepoint_root = os.getenv('gscf_sharepoint_root')
    gscf_site_url = os.getenv('gscf_site_url')
    gscf_library = os.getenv('gscf_library')
    gscf_folders = os.getenv('gscf_folders')
    gscf_folders_TS = os.getenv('gscf_folders_TS')

    print('gscf_folders ::', gscf_folders)
    print('gscf_folders_TS ::', gscf_folders_TS)

    access_token = get_access_token(gscf_tenant_id, gscf_client_id, gscf_client_secret)
    if not access_token:
        return

    site_id = get_site_id(access_token, gscf_sharepoint_root, gscf_site_url)
    if not site_id:
        return

    drive_id = get_drive_id(access_token, site_id, gscf_library)
    if not drive_id:
        return

    # Download ppt_excel.xlsx from gscf_folders
    folder_contents = get_folder_id(access_token, site_id, drive_id, gscf_folders)
    if not folder_contents:
        print(f'folder_contents for {gscf_folders} ::', folder_contents)
        return

    ppt_excel_file = next((item for item in folder_contents if 'file' in item and item['name'] == 'ppt_excel.xlsx'), None)
    if ppt_excel_file:
        ppt_excel_content = download_file(access_token, site_id, drive_id, ppt_excel_file['id'])
        if ppt_excel_content:
            print("Downloaded ppt_excel.xlsx")

            MY_Historical_values = pd.read_excel(BytesIO(ppt_excel_content), engine='openpyxl', dtype='object', sheet_name=None)
            ppt_excel = pd.read_excel(BytesIO(ppt_excel_content), sheet_name="Additive - YT06")
            PTtransfer = pd.read_excel(BytesIO(ppt_excel_content), sheet_name="Primary Transport - YT07")
            Bio_diesel = pd.read_excel(BytesIO(ppt_excel_content), sheet_name="Hydrocarbon Biodiesel B100")
            
        else:
            print("Failed to download ppt_excel.xlsx")
            ppt_excel = PTtransfer = MY_Historical_values = None
    else:
        print("File 'ppt_excel.xlsx' not found in", gscf_folders)
        ppt_excel = PTtransfer = MY_Historical_values = None



    # Download ppt_excel.xlsx from gscf_folders
    folder_contents = get_folder_id(access_token, site_id, drive_id, gscf_folders)
    if not folder_contents:
        print(f'folder_contents for {gscf_folders} ::', folder_contents)
        return


    Mapping_quotation_codes_file = next((item for item in folder_contents if 'file' in item and item['name'] == 'Mapping for Quotation codes.xlsx'), None)
    if Mapping_quotation_codes_file:
        Mapping_quotation_codes_content = download_file(access_token, site_id, drive_id, Mapping_quotation_codes_file['id'])
        if Mapping_quotation_codes_content:
            print("Downloaded Mapping_quotation_codes.xlsx")
            # MY_Historical_values = pd.read_excel(BytesIO(ppt_excel_content), engine='openpyxl', dtype='object', sheet_name=None)

            Mapping_quotation_codes = pd.read_excel(BytesIO(Mapping_quotation_codes_content), header=1)
            print("sharepoint connection file 255")
            print(Mapping_quotation_codes.columns)
            print("sharepoint connection file 257")
            print(Mapping_quotation_codes.head(4))
            
        else:
            print("Failed to download ppt_excel.xlsx")
            ppt_excel = PTtransfer = MY_Historical_values = None
    else:
        print("File 'ppt_excel.xlsx' not found in", gscf_folders)
        ppt_excel = PTtransfer = MY_Historical_values = None


    # Download T&S cockpit.xlsx from gscf_folders_TS
    folder_contents_TS = get_folder_id(access_token, site_id, drive_id, gscf_folders_TS)
    if not folder_contents_TS:
        print(f'folder_contents for {gscf_folders_TS} ::', folder_contents_TS)
        return

    ts_cockpit_file = next((item for item in folder_contents_TS if 'file' in item and item['name'] == 'T&S cockpit.xlsx'), None)
    if ts_cockpit_file:
        ts_cockpit_content = download_file(access_token, site_id, drive_id, ts_cockpit_file['id'])
        if ts_cockpit_content:
            print("Downloaded T&S cockpit.xlsx")
            depot_mapping = pd.read_excel(BytesIO(ts_cockpit_content), sheet_name="Depot Mapping")
        else:
            print("Failed to download T&S cockpit.xlsx")
            depot_mapping = None
    else:
        print("File 'T&S cockpit.xlsx' not found in", gscf_folders_TS)
        depot_mapping = None

    print('Successfully loaded files from Sharepoint for Malaysia.')
    print("***************************************")

    return Mapping_quotation_codes ,Bio_diesel, ppt_excel, PTtransfer, depot_mapping, MY_Historical_values
