import telebot
import requests
import traceback
from telebot import types
from configs import *
from translate import Translator as GoogleTranslator


bot = telebot.TeleBot(TOKEN)
src = 'en'
dest = 'ru'
translator = GoogleTranslator(to_lang=dest, from_lang=src)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}, для получении цитаты выбери команду /quote')


@bot.message_handler(commands=['quote'])
def send_quote(message):
    quote = get_quote()
    bot.reply_to(message, quote)


def get_quote():
    url = URL

    try:
        response = requests.get(url, verify=True)
        response.raise_for_status()

        data = response.json()
        quote_text_en = data['content']
        author_en = data['author']

        quote_text_ru = translator.translate(quote_text_en)
        author_ru = translator.translate(author_en)

        return f'Цитата: {quote_text_ru} \n Автор: {author_ru}'
    except Exception as e:
        # return f'Ошибка: {str(e)}'
        traceback.print_exc()
        bot.send_message(message.chat.id, f'Ошибка:  ')


@bot.message_handler(func=lambda message: True)
def user_write(message):
    user_text = message.text.lower()

    if user_text == 'i love you' or user_text == 'я люблю тебя':
        bot.reply_to(message, 'Я польщен 🥹 )')
    else:
        bot.send_message(message.chat.id, f'Лучше мудрости добавь в свою жизнь, а не простые слова 😉 )'
                                          f' И выбери команду /quote')


if __name__ == "__main__":
    bot.polling(none_stop=True)