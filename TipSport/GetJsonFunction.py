import requests
import json
import pandas as pd
from PostFunction import *
from deep_translator import GoogleTranslator

def translate_to_english(text):
    translator = GoogleTranslator(source='czech', target='english')
    translation = translator.translate(text)
    return translation

def GetJson(u, NameOfJson):
    NameOfJson=translate_to_english(NameOfJson)
    url = u
    data = get_data(url)

    base_url = 'https://www.tipsport.cz'
    response = requests.get(base_url)
    cookies = response.cookies
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Referer': base_url,
    }

    match_data = []

    total_competitions = data["offerSuperSports"][0]["tabs"][0]["offerCompetitionAnnuals"]
    for competition in total_competitions:
        compet_title = translate_to_english(competition["name"])
        matches = competition["matches"]
        for match in matches:
            match_title = translate_to_english(match["name"])
            match_url = base_url + match["matchUrl"]
            match_id = match["id"]
            
            response = requests.get(match_url)
            id = match_id
            r = requests.get(f'https://www.tipsport.cz/rest/offer/v1/matches/{id}/event-tables?fromResults=false', cookies=cookies, headers=headers)
            raw_data = r.text
            ma = json.loads(raw_data)
            
            odds_data = []
            for eventTable in ma["eventTables"]:
                market_title = translate_to_english(eventTable["name"])
                boxes = eventTable["boxes"]
                for box in boxes:
                    cells = box["cells"]
                    for cell in cells:
                        name = translate_to_english(cell["name"])
                        odd = {
                            "Name": name,
                            "Odd value": cell["odd"]
                        }
                        odds_data.append({"Market Title": market_title, 'Odds': odd})
            
            match = {
                "Competition Title": compet_title,
                "Match ID": match_id,
                "Match Title": match_title,
                "Match URL": match_url,
                "Match odds": odds_data
            }
            match_data.append(match)

    df = pd.DataFrame(match_data)
    json_data = df.to_json(orient='records')

    formatted_json = json.dumps(json.loads(json_data), indent=4)
    print(formatted_json)

    with open(f'{NameOfJson}.json', 'w') as file:
        file.write(formatted_json)
