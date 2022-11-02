import json
import requests
import telebot
from Get_Adress_Hotel import get_adress_hotel
from get_region_id import get_region
from photo_hotel import photo_hotel

bot = telebot.TeleBot('5554118297:AAGarcBl_40FviVp0lmmoKYNFM31Q3VKumw')

def lowprise(city, number_hotel, number_photo, chat_id) -> None:
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": get_region(city)},
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
        "sort": "PRICE_LOW_TO_HIGH",
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "10ee6bda01msh92b967849bb4496p12cc57jsn6d564d6b3eb8",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    todos = json.loads(response.text)
    with open('lowprice.json', 'w') as file:
        json.dump(todos, file, indent=4)

    with open('lowprice.json') as json_file:
        data = json.load(json_file)

        a = data["data"]["propertySearch"]["properties"]
        b = 0
        for i in a:
            bot.send_message(chat_id, "Отель номер {number}".format(number=b+1))
            bot.send_message(chat_id, 'Название: {title}'.format(title=i['name']))
            bot.send_message(chat_id, 'Адресс отеля: {adress}'.format(adress=get_adress_hotel(i["id"])))
            bot.send_message(chat_id, 'Расстояние до центра: {distance} {value}'.format(
                distance=i['destinationInfo']['distanceFromDestination']['value'],
                value=i['destinationInfo']['distanceFromDestination']['unit']))
            bot.send_message(chat_id, 'Цена за ночь:{cost}'.format(cost=i["mapMarker"]["label"]))
            if number_photo!='Нет':
                photo = photo_hotel(i['id'], number_photo)
                for i in photo:
                    bot.send_photo(chat_id, i)
            else:
                number_photo='Нет'
            bot.send_message(chat_id, '='*80)
            b += 1
            if b == number_hotel:
                break