import requests
import os
from dotenv import load_dotenv


def get_site_id(access_token):
    load_dotenv()

    print("Inside get site id function")
    ca_site_url = os.getenv('ca_site_url')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    # Construct the URL without the leading slash
    response = requests.get(f'https://graph.microsoft.com/v1.0/sites{ca_site_url}', headers=headers)
    
    if response.status_code == 200:
        site = response.json()
        print('site ::', site)
        return site['id']
    else:
        print('Error:', response.json())
        return None

# Example usage
access_token = 'your_access_token_here'
site_id = get_site_id(access_token)
print('Site ID:', site_id)



# def get_site_id(access_token):
#     load_dotenv()

#     print("Inside get site id function")
#     ca_site_url = os.getenv('ca_site_url')
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/json'
#     }
#     response = requests.get(f'https://graph.microsoft.com/v1.0/sites/{ca_site_url}', headers=headers)
    
#     site = response.json()
#     print('site ::', site)
#     return site['id']

def get_drive_id(access_token, site_id):
    print("Inside get drive id function")

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives', headers=headers)
    drives = response.json()

    print("error of id is in sharepoint_api file")
    return drives['value'][0]['id']

def get_file_content(access_token, drive_id, file_path):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f'https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{file_path}:/content', headers=headers)
    return response.content