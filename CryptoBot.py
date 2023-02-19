import telebot
from config import keys, TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Добро пожаловать!' \
        '\nЧтобы начать работу Вам нужно: ' \
        '\nВвести название валюты для конвертации, ' \
        '\nназвание валюты в которую конвертируем и количество конвертируемой валюты.' \
        '\nПосмотреть список доступных валют для конвертации:/currency'
    bot.reply_to(message, text)



@bot.message_handler(commands=['currency'])
def currency(message: telebot.types.Message):
    text = 'Доступные валюты для конвертации: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    try:
        currency = message.text.split(' ')

        if len(currency) >3:
            raise APIException('Слишком много символов!')

        quote, base, amount = currency
        total_base = Converter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя!\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду!\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} : {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()