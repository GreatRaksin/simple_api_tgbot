import telebot
from stuff import *  # импортировать все функции из файла stuff.py

import os

bot = telebot.TeleBot(os.environ.get('KEY'))

answers = {
    'git': 'Введи запрос для поиска в формате "GIT Запрос Язык_Программирования" и я дам тебе ссылки на 5 случайных репозиториев',
    'help': 'Я умею искать по гитхабу и повторять слова за тобой. Чтобы узнать, как искать, напиши мне слово git',
}


@bot.message_handler(commands=['start', 'help', 'dog'])
def commands(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, f'Привет, {message.chat.username}!')
        bot.send_message(message.chat.id, text=read_file('msg_templates/start.html'), parse_mode='html')
    elif message.text == '/help':
        bot.send_message(message.chat.id, answers['help'])
    elif message.text == '/dog':
        img = get_image()
        bot.send_photo(message.chat.id, photo=img)


@bot.message_handler(commands=['weather'])
def button_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = telebot.types.KeyboardButton('Поделиться локацией', request_location=True)
    markup.add(btn)
    bot.send_message(message.chat.id, 'Поделись со мной своей локацией, пожалуйста.', reply_markup=markup)


@bot.message_handler(content_types=['location'])
def contact(message):
    if message.location is not None:
        lat = message.location.latitude
        long = message.location.longitude
        city = get_city(lat, long)
        msg = f'Твой город: {city["city"]}'
        ans = get_forecast(lat, long)
        bot.send_message(message.chat.id, msg)
        bot.send_message(message.chat.id, ans)


@bot.message_handler(content_types=['text'])  # декоратор
def repeat_message(message):
    if message.text.startswith('GIT'):
        msg = message.text.split()
        res = git_search(msg[1], msg[2])
        msg = "Вот, что я смог найти:\n" + res
        bot.send_message(message.chat.id, text=msg, parse_mode='html')