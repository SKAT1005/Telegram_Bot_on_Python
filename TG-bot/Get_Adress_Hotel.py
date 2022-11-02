import  json
import requests

def get_adress_hotel(prop_id: str)->str:
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": prop_id
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "10ee6bda01msh92b967849bb4496p12cc57jsn6d564d6b3eb8",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    todos = json.loads(response.text)
    with open('get_addres_hotel.json', 'w') as file:
        json.dump(todos, file, indent=4)

    with open('get_addres_hotel.json') as json_file:
        data = json.load(json_file)

        a = data["data"]["propertyInfo"]["summary"]["location"]["address"]["addressLine"]
        return a

