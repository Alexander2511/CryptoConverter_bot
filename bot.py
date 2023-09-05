import telebot
from config import TOKEN, keys
from exception import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


# Обработчики команд
@bot.message_handler(commands=['start', 'help'])
def handle_start_command(message):
    handle_start(message)


@bot.message_handler(commands=['values'])
def handle_values_command(message):
    handle_values(message)


# Обработка ввода текста
@bot.message_handler(content_types=['text', ])
def handle_text(message):
    handle_conversion(message)


# Функции обработки команд бота
def handle_start(message):
    text = 'Для конвертации инересующих Вас валют необхдимо внести данные в следующем формате (через пробел):' \
           ' \n- <Название валюты, с которй хотим конвертировать >  \n- <Название валюты, в которую конвертируем> ' \
           ' \n- <Количество первой валюты>\n \
           Список доступных валют: /values'
    bot.reply_to(message, text)


def handle_values(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


def handle_conversion(message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверно введены параметры')

        base, quote, amount = values
        amount = float(amount)

        if amount < 0:
            raise APIException('Количество не может быть отрицательным')

        total_amount = CryptoConverter.get_total_amount(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Произошла ошибка: \n{e}')
    else:
        text = f'Сумма {amount} {base} в {quote}: {total_amount} {quote}'
        bot.send_message(message.chat.id, text)


# Запуск бота
bot.polling(none_stop=True)
