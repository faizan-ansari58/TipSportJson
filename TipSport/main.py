from GetJsonFunction import *

import requests
import json
base_url = 'https://www.tipsport.cz'
response = requests.get(base_url)
cookies = response.cookies
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Referer': base_url,
}

second_page_url = 'https://www.tipsport.cz/rest/offer/v4/sports?fromResults=true'
response2 = requests.get(second_page_url, headers=headers, cookies=cookies)

raw_data = response2.content
data = json.loads(raw_data)

league_url = []
league_title = []

for child in range(0,len(data["data"]["children"])):
    for i in range(0,len(data["data"]["children"][child]["children"])):
        #for favourite leagues types
        league_url.append(base_url + data["data"]["children"][child]["children"][i]["url"])
        league_title.append(data["data"]["children"][child]["children"][i]["title"])   
            
for i in range(24,len(league_url)):
    GetJson(league_url[i],league_title[i])
