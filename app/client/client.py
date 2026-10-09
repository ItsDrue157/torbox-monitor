import requests
from pathlib import Path
import os 
from dotenv import load_dotenv

path_dotenv = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(path_dotenv)

token_api = os.getenv("torbox_token")



def get_downloads():
    url = "https://api.torbox.app/v1/api/torrents/mylist"


    headers = {
        "Authorization": f"Bearer {token_api}",
        'Content-Type': 'application/json'
    }
    site = requests.get(url,headers=headers)
    data = site.json()

        
    # if site.status_code == 200:   
    #     print(data['data'])

    # else:
    #     print(f'Error: {site.status_code}')

    donwloads_filtrados = []
    downloads = data["data"]

    for download in downloads:
        donwloads_filtrados.append({
            "id":download["id"],
            "name": download["name"],
            "download_state":download["download_state"],
            "create_at":download["created_at"],
            "progress": download["progress"],
            "eta":download["eta"]

        })

    return donwloads_filtrados

