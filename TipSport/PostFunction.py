import requests
import json

def get_data(link):
    response = requests.get(link)
    cookies = response.cookies
    id_value = link.split('-')[-1]
    payload = {
        "results": False,
        "highlightAnyTime": False,
        "limit": 225,
        "type": "SUPERSPORT",
        "id": int(id_value),
        "fulltexts": [],
        "matchIds": [],
        "matchViewFilters": [],
        "url": str(link)
    }   
    querystring = {"limit": "225"}
    url = 'https://www.tipsport.cz/rest/offer/v2/offer'
    res = requests.request("POST", url, json=payload, params=querystring, cookies=cookies)
    raw_data = res.text
    data = json.loads(raw_data)
    return data
