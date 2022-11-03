import telebot

from lowprice import lowprise

bot = telebot.TeleBot('5554118297:AAGarcBl_40FviVp0lmmoKYNFM31Q3VKumw')
alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
max_hotels = 8
max_photo = 20


def get_number_photo(message, list, chat_id):
    x = message.text
    if 0 < int(x) < max_photo:
        list.append(x)
        lowprise(str(list[0]), int(list[1]), int(list[2]), chat_id)
    else:
        msg = bot.send_message(message.chat.id, "Введите число, которое больше 0{number}".format(number=max_photo))
        bot.register_next_step_handler(msg, get_number_photo, list, chat_id)


def ask_about_photo(message, list, chat_id):
    x = message.text
    if x == 'Да' or x == 'да':
        msg = bot.send_message(message.chat.id, 'Введите сколько фотографий отелей хотите посмотреть')
        bot.register_next_step_handler(msg, get_number_photo, list, chat_id)
    elif x == 'Нет' or x == 'Нет':
        list.append('Нет')
        lowprise(str(list[0]), int(list[1]), str(list[2]), chat_id=1288389919)
    else:
        msg = bot.send_message(message.chat.id, 'Да или Нет')
        bot.register_next_step_handler(msg, ask_about_photo, list, chat_id)


def get_number_hotel(message, list, chat_id):
    x = message.text
    if 0 < int(x) < max_hotels:
        list.append(x)
        msg = bot.send_message(message.chat.id,
                               "Хотели бы вы посмотреть фотографии отеля? Введите 'Да', чтобы посмотреть и 'Нет', если не хотите смотреть")
        bot.register_next_step_handler(msg, ask_about_photo, list, chat_id)
    else:
        msg = bot.send_message(message.chat.id,
                               "Введите число, которое больше 0 и меньше либо равно {number}".format(number=max_hotels))
        bot.register_next_step_handler(msg, get_number_hotel, list, chat_id)


def get_city(message, list, chat_id):
    x = message.text
    a = True
    x = "".join(x.split())
    for i in x:
        if i not in alphabet:
            a = False
    if a:
        list.append(x)
        msg = bot.send_message(message.chat.id, "Введите сколько отелей хотите посмотреть")
        bot.register_next_step_handler(msg, get_number_hotel, list, chat_id)
    else:
        msg = bot.send_message(message.chat.id, "Введите Название английскими буквами.")
        bot.register_next_step_handler(msg, get_city, list, chat_id)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    '''Метод для получения сообщений и ответа на них.'''
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")

    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет или /lowprice")

    elif message.text == '/lowprice':
        list = []
        chat_id = message.chat.id
        msg = bot.send_message(message.chat.id, "Введите город, в который вы хотите поехать на английском языке")
        bot.register_next_step_handler(msg, get_city, list, chat_id)

    elif message.text == '/start':
        bot.send_message(message.from_user.id,
                         "Привет! Я - Телеграм-бот для поиска отелей. "
                         "Пока знаю только команду 'Привет' и '/help', но дальше я буду улучшаться")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)