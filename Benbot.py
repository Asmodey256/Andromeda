import telebot
from config import keys, TOKEN
from extensions import APIEException, ValutConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help (message: telebot.types.Message):
    text = "Добрый день. Чтобы начать работу введите комманду боту в следующей форме: \n <Имя валюты> \
    <В какою валюты перевести> \
    <Колличество валюты> \n <Список доступных валют: /values>"
    bot.reply_to(message, text)

@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise APIEException("Должно быть три параметра")

        quote, base, amount = values

        total_base = ValutConverter.get_price(quote, base, amount)

    except APIEException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")
    except  Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f"Цена {amount} {quote} в {base} - {total_base}"
        bot.send_message(message.chat.id, text)

bot.polling()