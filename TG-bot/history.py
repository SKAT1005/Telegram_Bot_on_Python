import telebot


bot = telebot.TeleBot('5554118297:AAGarcBl_40FviVp0lmmoKYNFM31Q3VKumw')
def history(chat_id: int)-> None:
    """Функция выводит дату запросов, историю запросов пользователя и отели, которые бот нашел по этим запросам

    :param chat_id: Id чата с пользователем
    :return: None
    """
    b=0
    with open('history.text', encoding='utf-8') as history:
        for i in history:
            a=i.split('|')
            if int(a[0])==chat_id:
                a.remove(a[0])
                bot.send_message(chat_id,'\n'.join(a))
                b+=1
        if b==0:
            bot.send_message(chat_id, 'К сожалению вы еще не делали запросов.')