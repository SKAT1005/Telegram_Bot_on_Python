import json

import requests


def get_region(city: str) -> str:
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"

    querystring = {"q": city}

    headers = {
        "X-RapidAPI-Key": "10ee6bda01msh92b967849bb4496p12cc57jsn6d564d6b3eb8",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    todos = json.loads(response.text)
    with open('get_region_id.json', 'w') as file:
        json.dump(todos, file, indent=4)
    with open('get_region_id.json') as json_file:
        data = json.load(json_file)
        a = data["sr"][0]['gaiaId']
        return str(a)
