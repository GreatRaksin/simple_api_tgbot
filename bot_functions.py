import telebot
from stuff import *  # импортировать все функции из файла stuff.py

import os

bot = telebot.TeleBot(os.environ.get('KEY'))


@bot.message_handler(commands=['start', 'help', 'dog'])
def commands(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, f'Привет, {message.chat.username}!')
        bot.send_message(message.chat.id, text=read_file('msg_templates/start.html'), parse_mode='html')
    elif message.text == '/help':
        bot.send_message(message.chat.id, text=read_file('msg_templates/start.html'), parse_mode='html')
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
        bot.send_message(message.chat.id, text=ans, parse_mode='html')


@bot.message_handler(content_types=['text'])  # декоратор
def repeat_message(message):
    if message.text.startswith('GIT'):
        msg = message.text.split()
        res = git_search(msg[1], msg[2])
        msg = "Вот, что я смог найти:\n" + res
        bot.send_message(message.chat.id, text=msg, parse_mode='html')