import telebot
from config import keys,TOKEN
from extensions import APIException, MoneyConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите комманду боту в следующем формате:\n" \
           "<имя валюты>" \
           "<в какую валюту перевести>" \
           "<количество переводимой ввалюты>\nУвидеть списоквсех доступных валют : \n /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values (message: telebot.types.Message):
    text = 'Доступые валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise  APIException('Слишком много параметров')

        quote, base, amount = values
        total_base = MoneyConverter.convert(quote, base, amount)
    except  APIException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'не удалось обработать команду \n{e}')
    else:

        text = f'Цена {amount} {quote} в {base} - {total_base} '
        bot.send_message(message.chat.id, text)

bot.polling()
