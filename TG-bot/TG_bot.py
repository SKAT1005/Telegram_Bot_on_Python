import telebot
from telebot import types

from bestdeal import bestdeal
from highprice import hightprice
from history import history
from lowprice import lowprice

bot = telebot.TeleBot('5554118297:AAGarcBl_40FviVp0lmmoKYNFM31Q3VKumw')
alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
max_hotels = 20
max_photo = 20


def get_number_photo(message, lst, chat_id):
    """Функция, принмает кол-во фотогравий отеля, которые хочет посмотреть пользователь.
    Провяется первый элемент списка lst.

    Если элемент равняется lp:
    Вызывается функция lowprice из файла lowprice.py

    Если элемент равняется hp:
    Вызывается функция hightprice из файла hightprice.py

    Если элемент равняется bd:
    Вызывается функция bestdeal из файла bestdeal.py

    :param message: Сообщение пользователя
    :param lst: список
    :param chat_id: id чата с пользователем
    :return: None
    """
    x = message.text
    if 0 < int(x) <= max_photo:
        lst.append(x)
        if lst[0] == 'lp':
            lowprice(lst[1], lst[2], lst[3], str(lst[4]), int(lst[5]), int(lst[6]), chat_id)
        elif lst[0] == 'hp':
            hightprice(lst[1], lst[2], lst[3], str(lst[4]), int(lst[5]), int(lst[6]), chat_id)
        else:
            bestdeal(lst[1], lst[2], lst[3], str(lst[4]), int(lst[5]), int(lst[6]), int(lst[7]), int(lst[8]),
                     int(lst[9]), int(lst[10]), chat_id)
    else:
        msg = bot.send_message(message.chat.id, "Введите число, которое больше 0 и меньше "
                                                "{number}".format(number=max_photo))
        bot.register_next_step_handler(msg, get_number_photo, lst, chat_id)


def ask_about_photo(message, lst, chat_id):
    """Функция, принмает ответ от пользователя хочет он посмотреть фотографии отеля или нет.
    Если ответ положительный вызыватеся функция get_number_photo
    Если ответ отрицательный провяется первый элемент списка lst.

    Если элемент равняется lp:
    Вызывается функция lowprice из файла lowprice.py

    Если элемент равняется hp:
    Вызывается функция hightprice из файла hightprice.py

    Если элемент равняется bd:
    Вызывается функция bestdeal из файла bestdeal.py

    :param message: Сообщение пользователя
    :param lst: список
    :param chat_id: id чата с пользователем
    :return: None """

    x = message.text
    if x == 'Да' or x == 'да':
        msg = bot.send_message(message.chat.id, 'Введите сколько фотографий отелей хотите'
                                                ' посмотреть(больше 0 и меньше {number})'.format(number=max_photo))
        bot.register_next_step_handler(msg, get_number_photo, lst, chat_id)
    elif x == 'Нет' or x == 'нет':
        if lst[0] == 'lp':
            lst.append('Нет')
            lowprice(lst[1], lst[2], lst[3], str(lst[4]), int(lst[5]), str(lst[6]), chat_id)
        elif lst[0] == 'hp':
            lst.append('Нет')
            hightprice(lst[1], lst[2], lst[3], str(lst[4]), int(lst[5]), str(lst[6]), chat_id)
        elif lst[0] == 'bd':
            lst.append('Нет')
            bestdeal(lst[1], lst[2], lst[3], str(lst[4]), int(lst[5]), int(lst[6]), int(lst[7]), int(lst[8]),
                     int(lst[9]), lst[10], chat_id)
    else:
        msg = bot.send_message(message.chat.id, 'Введите Да или Нет')
        bot.register_next_step_handler(msg, ask_about_photo, lst, chat_id)


def get_number_hotel(message, lst, chat_id):
    """Функция, для определения кол-ва отелей, которые хчет посмотреть пользователь.
    После завершения вызывает функцию ask_about_photo

    :param message: Сообщение пользователя
    :param lst: список
    :param chat_id: id чата с пользователем
    :return: None """
    x = message.text
    if x in '0123456789':
        if 0 < int(x) <= max_hotels:
            lst.append(x)
            msg = bot.send_message(message.chat.id,
                                   "Хотели бы вы посмотреть фотографии отеля? "
                                   "Введите 'Да', чтобы посмотреть и 'Нет', если не хотите смотреть")
            bot.register_next_step_handler(msg, ask_about_photo, lst, chat_id)
        else:
            msg = bot.send_message(message.chat.id,
                                   "Введите число, которое больше 0 и меньше либо равно {number}".format(
                                       number=max_hotels))
            bot.register_next_step_handler(msg, get_number_hotel, lst, chat_id)
    else:
        msg = bot.send_message(message.chat.id,
                               "Введите число, которое больше 0 и меньше либо равно {number}".format(number=max_hotels))
        bot.register_next_step_handler(msg, get_number_hotel, lst, chat_id)


def get_distance_range(message, lst, chat_id):
    """Функция, для определения промежутка допустимой дистанции от отлея до центра.
    После завершения вызывает функцию get_city

    :param message: Сообщение пользователя
    :param lst: список
    :param chat_id: id чата с пользователем
    :return: None """

    x = message.text
    x = x.split('-')
    if len(x) == 2 and 0 <= int(x[0]) < int(x[1]):
        lst.append(int(x[0]))
        lst.append(int(x[1]))
        msg = bot.send_message(message.chat.id,
                               "Введите сколько отелей хотите посмотреть(больше 0 и меньше либо равное {number})".format(
                                   number=max_hotels))
        bot.register_next_step_handler(msg, get_number_hotel, lst, chat_id)
    else:
        msg = bot.send_message(message.chat.id,
                               "Расстояния должны быть больше или равно 0, разделены "
                               "'-' и первое число должно быть меньше второго")
        bot.register_next_step_handler(msg, get_distance_range, lst, chat_id)


def get_price_range(message, lst, chat_id):
    """Функция для опрееделения промежутка цены за отель,
    После завершения вызывает функцию get_distance_range


    :param message: Сообщение пользователя
    :param lst: список
    :param chat_id: id чата с пользователем
    :return: None"""

    x = message.text
    x = x.split('-')
    if len(x) == 2 and 0 <= int(x[0]) < int(x[1]):
        lst.append(int(x[0]))
        lst.append(int(x[1]))
        msg = bot.send_message(message.chat.id,
                               "Введите диапазон расстояний от центра,( расстояния должны быть больше 0,"
                               " разделены '-' и первое число должно быть меньше второго)")
        bot.register_next_step_handler(msg, get_distance_range, lst, chat_id)
    else:
        msg = bot.send_message(message.chat.id,
                               "Цены должны быть больше или равно 0, разделены "
                               "'-' и первое число должно быть меньше второго")
        bot.register_next_step_handler(msg, get_price_range, lst, chat_id)


def get_city(message, lst, chat_id):
    """Функция для определения города, в котором пользователь ищет отель

    Провяется первый элемент списка lst. Если элемент равняется lp или hp:
    Вызывается функция get_number_hotel

    Если элемент равняется bd:
    Вызывается функция get_price_range

    :param message: Сообщение пользователя
    :param lst: список
    :param chat_id: id чата с пользователем
    :return: None
    """
    x = message.text
    x = "".join(x.split())
    for i in x:
        if i not in alphabet:
            msg = bot.send_message(message.chat.id, "Введите Название английскими буквами.")
            bot.register_next_step_handler(msg, get_city, lst, chat_id)

    lst.append(x)
    if lst[0] == 'lp' or lst[0] == 'hp':
        msg = bot.send_message(message.chat.id,
                               "Введите сколько отелей хотите посмотреть(больше 0 и меньше либо равное {number})".format(
                                   number=max_hotels))
        bot.register_next_step_handler(msg, get_number_hotel, lst, chat_id)
    elif lst[0] == 'bd':
        msg = bot.send_message(message.chat.id,
                               "Введите диапазон цен,( цены должны быть больше 0,"
                               " разделены '-' и первое число должно быть меньше второго)")
        bot.register_next_step_handler(msg, get_price_range, lst, chat_id)


def get_check_in_and_check_out(message, lst, chat_id):
    """Функция, для определения даты пребывания пользователя в отеле. После завершения вызывает функцию get_city

    :param message: Сообщение пользователя
    :param lst: список
    :param chat_id: id чата с пользователем
    :return: None """
    x = message.text
    a = x.split()
    if len(a) != 2:
        msg = bot.send_message(message.chat.id, "Даты должны разделяться пробелом и иметь формат (YYYY-MM-DD).")
        bot.register_next_step_handler(msg, get_check_in_and_check_out, lst, chat_id)
    else:
        a0 = a[0].split('-')
        a1 = a[1].split('-')
        if len(a0[2]) == 2 and len(a0[1]) == 2 and len(a0[0]) == 4 \
                and len(a1[2]) == 2 and len(a1[1]) == 2 and len(a1[0]) == 4:
            if int(a0[1]) <= 12 or int(a1[1]) <= 12:
                if len(a0[0]) != 4 or len(a0[1]) != 2 or len(a0[2]) != 2 or len(a1[0]) != 4 or len(a1[1]) != 2 or len(
                        a1[1]) != 2:
                    msg = bot.send_message(message.chat.id, "Введите период на который вы хотите поехат в формате"
                                                            "(YYYY-MM-DD). Если месяц или день "
                                                            "заканчивается на 1 цифру, то перед ней посавьте 0 Например:\n"
                                                            "2022-9-1 2022-10-1 Неправильно\n"
                                                            "2022-09-01 2022-10-1 Правильно")
                    bot.register_next_step_handler(msg, get_check_in_and_check_out, lst, chat_id)
                c = 0
                if int(a0[0]) == int(a1[0]) and int(a0[1]) == int(a1[1]):
                    c = int(a1[2]) - int(a0[2])
                    lst.append(a[0])
                    lst.append(a[1])
                    lst.append(c)
                else:
                    if int(a0[1]) == 1 or int(a0[1]) == 3 or int(a0[1]) == 5 or int(a0[1]) == 7 or int(
                            a0[1]) == 8 or int(
                            a0[1]) == 10 or int(a0[1]) == 12:
                        c = 31 - int(a0[2]) + int(a1[2])
                        lst.append(a[0])
                        lst.append(a[1])
                        lst.append(c)
                    elif int(a0[1]) == 4 or int(a0[1]) == 6 or int(a0[1]) == 9 or int(a0[1]) == 11:
                        c = 30 - int(a0[2]) + int(a1[2])
                        lst.append(a[0])
                        lst.append(a[1])
                        lst.append(c)
                    else:
                        c = 28 - int(a0[2]) + int(a1[2])
                        lst.append(a[0])
                        lst.append(a[1])
                        lst.append(c)
                msg = bot.send_message(message.chat.id,
                                       "Введите город, в который вы хотите поехать на английском языке."
                                       " Поиск по России временно недоступен.")
                bot.register_next_step_handler(msg, get_city, lst, chat_id)
            else:
                msg = bot.send_message(message.chat.id,
                                       "Месяцев только 12, введите число, которое больше нуля и меньше или равно 12")
                bot.register_next_step_handler(msg, get_check_in_and_check_out, lst, chat_id)
        else:
            msg = bot.send_message(message.chat.id, "Месяц и день должны содержать 2 цифры, а год 4 цифры"
                                                    "Если месяц равняется 1, но поставьте перед ним 0. Например:\n"
                                                    "22-9-1 2022-10-1 Неправильно\n"
                                                    "2022-09-01 2022-10-1 Правильно")
            bot.register_next_step_handler(msg, get_check_in_and_check_out, lst, chat_id)


@bot.message_handler(commands=['start'])
def start(message):
    """
    Метод для создания создания кнопок бота. После создания всех кнопок вызывает метод get_text_messages

    :param message: Cообщение пользователя
    :return: None
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/help")
    btn2 = types.KeyboardButton("/lowprice")
    btn3 = types.KeyboardButton("/hightprice")
    btn4 = types.KeyboardButton("/bestdeal")
    btn5 = types.KeyboardButton("/history")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Спасибо, что пользуетесь услугами нашей компании".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    '''Метод для получения команд от пользователя, который расспазнает 5 комманд.
    В случае если ни одна команда не подходит к сообщению пользователя,
    бот сообщает пользователю это

    /help -- Выводит все доступные команды пользователя и их функционал

    /lowprice -- Создаёт список lst, которая содержит краткое название команды,
    создает переменную chat_id, которая содержит id чата с пользователем,
    cоздает переменную msg, которая содержит ответ пользователя
    и в функцию get_check_in_and_check_out передет 3 аргумента
    1 -- Сообщение пользователя
    2 -- Список lst
    3 -- chat_id

    /hightprice -- Создаёт список lst, которая содержит краткое название команды,
    создает переменную chat_id, которая содержит id чата с пользователем,
    cоздает переменную msg, которая содержит ответ пользователя
    и в функцию get_check_in_and_check_out передет 3 аргумента
    1 -- Сообщение пользователя
    2 -- Список lst
    3 -- chat_id

    /bestdeal -- Создаёт список lst, которая содержит краткое название команды,
    создает переменную chat_id, которая содержит id чата с пользователем,
    cоздает переменную msg, которая содержит ответ пользователя
    и в функцию get_check_in_and_check_out передет 3 аргумента
    1 -- Сообщение пользователя
    2 -- Список lst
    3 -- chat_id

    /history  -- Создает переменную chat_id, которая содержит id чата с пользователем
    и вызывает функцию history из файла history.py

    :param message: Сообщение пользователя
    :return: None
    '''
    if message.text == "/help":
        print(message.chat.id)
        bot.send_message(message.from_user.id, "Напишите /lowprice, чтобы узнать информацию о самых дешевых отелях\n"
                                               "/hightprice для того, чтобы узнать о самых дорогих отелях\n"
                                               "/bestdeal для того, чтобы указать диапазон цен и расстояния"
                                               " и увидеть подходящие вам отели,\n"
                                               "/history для того, чтобы узнать о истории своих запросов.")

    elif message.text == '/lowprice':
        lst = ['lp']
        chat_id = message.chat.id
        msg = bot.send_message(message.chat.id, "Введите период на который вы хотите поехать в формате"
                                                "(YYYY-MM-DD YYYY-MM-DD) если месяц или день "
                                                "заканчивается на 1 цифру, то перед ней посавьте 0 Например:\n"
                                                "2022-9-1 2022-10-1 Неправильно\n"
                                                "2022-09-01 2022-10-1 Правильно")
        bot.register_next_step_handler(msg, get_check_in_and_check_out, lst, chat_id)

    elif message.text == "/hightprice":
        lst = ['hp']
        chat_id = message.chat.id
        msg = bot.send_message(message.chat.id, "Введите период на который вы хотите поехать в формате"
                                                " (YYYY-MM-DD YYYY-MM-DD) если месяц или день "
                                                "заканчивается на 1 цифру, то перед ней посавьте 0 Например:\n"
                                                "2022-9-1 2022-10-1 Неправильно\n"
                                                "2022-09-01 2022-10-1 Правильно")
        bot.register_next_step_handler(msg, get_check_in_and_check_out, lst, chat_id)
    elif message.text == "/bestdeal":
        lst = ['bd']
        chat_id = message.chat.id
        msg = bot.send_message(message.chat.id, "Введите период на который вы хотите поехать в формате"
                                                " (YYYY-MM-DD YYYY-MM-DD) если месяц или день "
                                                "заканчивается на 1 цифру, то перед ней посавьте 0 Например:\n"
                                                "2022-9-1 2022-10-1 Неправильно\n"
                                                "2022-09-01 2022-10-1 Правильно")
        bot.register_next_step_handler(msg, get_check_in_and_check_out, lst, chat_id)
    elif message.text == '/history':
        chat_id = message.chat.id
        history(chat_id)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
