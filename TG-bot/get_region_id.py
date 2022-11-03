import json

import requests


def get_region(city: str) -> str:
    """Функция находит destinationId по названию города

    :param city: Название города, который надо найти
    :return: Если удалось найти город, возвращаят его destinationId.
    Если нет, возвращяет строку 1234
    """
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"

    querystring = {"query": city}

    headers = {
        "X-RapidAPI-Key": "fa25bc8374mshf68f100cb0a70d1p194921jsn020bfed70507",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    todos = json.loads(response.text)
    with open('get_region_id.json', 'w') as file:
        json.dump(todos, file, indent=4)
    with open('get_region_id.json') as json_file:
        data = json.load(json_file)
        a = data["suggestions"][0]['entities']
        if len(a)==0:
            return '1234'
        else:
            a = data["suggestions"][0]['entities']
            return str(a)