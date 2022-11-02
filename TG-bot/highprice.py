import json

import requests

url = "https://hotels4.p.rapidapi.com/properties/v2/list"

payload = {
    "currency": "USD",
    "eapid": 1,
    "locale": "en_US",
    "siteId": 300000001,
    "destination": {"regionId": "2621"},
    "checkInDate": {
        "day": 10,
        "month": 10,
        "year": 2022
    },
    "checkOutDate": {
        "day": 15,
        "month": 10,
        "year": 2022
    },
    "rooms": [
        {
            "adults": 2,
            "children": [{"age": 5}, {"age": 7}]
        }
    ],
    "resultsStartingIndex": 0,
    "resultsSize": 200,
    "sort": "PRICE_HIGH_TO_LOW",
}
headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "10ee6bda01msh92b967849bb4496p12cc57jsn6d564d6b3eb8",
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.request("POST", url, json=payload, headers=headers)

todos = json.loads(response.text)
with open('../highprice/hight_price.json', 'w') as file:
    json.dump(todos, file, indent=4)