import datetime
import json

import requests
import telebot

from config import bot_token, API_key
from get_region_id import get_region
from photo_hotel import photo_hotel

bot = telebot.TeleBot(bot_token())


def bestdeal(checkindate: str, checkoutdate: str,
             day: int, city: str, min_price: int,
             max_price: int,
             min_distance: int, max_distance: int,
             number_hotel: int,
             number_photo, chat_id) -> None:
    """Функция выводящяя Названия, адресса, сайты, расстояния до центра,
    цены за ночь, цены за весь период
    и фотографии отелей по фильтрам пользователя

    :param checkindate: Дата регистрации пользователя в отеле
    :param checkoutdate: Дата выписки пользователя из отеля
    :param day: Кол-во проведенных дней в отеле
    :param city: Город, в котором ищются отели
    :param min_price: Минимальная цена за ночь в отеле
    :param max_price: Максимальная цена за ночь в отеле
    :param min_distance: Минимальное расстояние от отеля до центра
    :param max_distance: Максимальное расстояние от отеля до центра
    :param number_hotel: Кол-во, выводимых отелей пользоватю
    :param number_photo: Кол-во фотографий, выводимых отелей пользоватю
    :param chat_id: ID чата с пользователем
    :return: None
    """
    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId": get_region(city),
                   "pageNumber": "1", "pageSize":
                       "200", "checkIn": checkindate,
                   "checkOut": checkoutdate,
                   "adults1": "1", "sortOrder":
                       "PRICE", "locale": "en_US",
                   "currency": "USD"}

    headers = {
        "X-RapidAPI-Key": API_key(),
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    todos = json.loads(response.text)
    with open('lowprice.json', 'w') as file:
        json.dump(todos, file, indent=4)

    with open('lowprice.json') as json_file:
        data = json.load(json_file)
        lst = []
        try:
            a = data["data"]["body"]["searchResults"]['results']
        except KeyError:
            bot.send_message(chat_id, "По вашему запросу ничего"
                                      "не удалось найти.")
            with open('history.text', 'a', encoding='utf-8') as history:
                history.write(
                    '{id}|Дата выполнения запроса: {date}|Команда: /lowprice|'
                    'Найденные отели: К сожалению'
                    'отелей найдено не было\n'.format(
                        id=chat_id,
                        date=datetime.date.today()))
        else:
            b = 0
            for i in range(number_hotel):
                lst.append(a[i]['name'])
                if min_price <= a[i]['ratePlan']['price']['exactCurrent'] <=\
                        max_price \
                        and min_distance <=\
                        float(a[i]['landmarks'][0]['distance'][:3]) <=\
                        max_distance:
                    b += 1
                    lst.append(a[i]['name'])
                    bot.send_message(chat_id, "Отель номер {number}".format(
                        number=i + 1))
                    bot.send_message(chat_id, 'Название: {title}'.format(
                        title=a[i]['name']))
                    bot.send_message(chat_id,
                                     'Адресс отеля:'
                                     '{streetAddress}, {locality},'
                                     '{postalCode}, {region}, {countryName}'
                                     .format(streetAddress=a[i]['address']
                                             ['streetAddress'],
                                             locality=a[i]['address']
                                             ['locality'],
                                             postalCode=a[i]['address']
                                             ['postalCode'],
                                             region=a[i]['address']
                                             ['region'],
                                             countryName=a[i]['address']
                                             ['countryName']))
                    bot.send_message(chat_id,
                                     'Сайт отеля: {site}'.format(
                                         site='https://www.hotels.com/ho'
                                              + str(a[i]['id']) + '/'))
                    bot.send_message(chat_id, 'Расстояние до центра:'
                                              '{distance}'.format(
                                                distance=a[i]['landmarks']
                                                [0]['distance']))
                    bot.send_message(chat_id, 'Цена за ночь: {cost}$'.format(
                        cost=a[i]['ratePlan']['price']['exactCurrent']))
                    bot.send_message(chat_id,
                                     'Цена все время: {totalcost}$'.format(
                                         totalcost=a[i]
                                         ['ratePlan']['price']
                                         ['exactCurrent'] * day))
                    if number_photo != 'Нет':
                        photo = photo_hotel(str(a[i]['id']), number_photo)
                        for p in photo:
                            bot.send_photo(chat_id, p)
                    else:
                        pass
    if b >= 1:
        with open('history.text', 'a', encoding='utf-8') as history:
            history.write(
                '{id}|Дата выполнения запроса:'
                '{date}|Команда:'
                '/bestdeal|Найденные отели:'
                '{hotels}\n'.format(
                    id=chat_id,
                    date=datetime.date.today(),
                    hotels=", ".join(lst)))
    else:
        bot.send_message(chat_id, "По вашему запросу"
                                  "ничего не удалось найти.")
        with open('history.text', 'a', encoding='utf-8') as history:
            history.write(
                '{id}|Дата выполнения запроса:'
                '{date}|Команда: /bestdeal|'
                'Найденные отели: К сожалению'
                'отелей найдено не было\n'.format(
                    id=13314,
                    date=datetime.date.today()))
