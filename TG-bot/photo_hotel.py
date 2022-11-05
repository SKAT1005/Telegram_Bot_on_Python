import json
import requests
from config import API_key
def photo_hotel(hotel_id: str, number)-> list:
    """Функция находит фотографии по Id отеля

    :param hotel_id: Id отеля
    :param number: Сколько фотографий нужно вывести
    :return: Список, состоящий из ссылок на фотографиии
    """
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": hotel_id}

    headers = {
        "X-RapidAPI-Key": API_key(),
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)

    todos = json.loads(response.text)
    with open('get_photo_hotel.json', 'w') as file:
        json.dump(todos, file, indent=4)

    with open('get_photo_hotel.json') as json_file:
        data = json.load(json_file)

        lst=[]
        for i in range(number):
            a=data['hotelImages'][i]['baseUrl']
            a=a.replace('{size}', 'w')
            lst.append(a)
    return lst