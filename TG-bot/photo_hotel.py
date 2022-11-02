import json
import requests
def photo_hotel(prop_id: str, number)-> list:
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
    with open('get_photo_hotel.json', 'w') as file:
        json.dump(todos, file, indent=4)

    with open('get_photo_hotel.json') as json_file:
        data = json.load(json_file)

        a = data["data"]["propertyInfo"]['propertyGallery']["images"]
        b=0
        lst=[]
        for i in a:

            lst.append(i['image']['url'])
            b+=1
            if b==number:
                break
    return lst