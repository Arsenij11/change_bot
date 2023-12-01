import telebot
from config import keys,TOKEN
from extensions import currencychecking,API,countofvalues,keyisnotexist,equalvalues

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Приветствую, {message.chat.username}.\nЭтот бот умеет возвращаать цену на определённое количество валюты.\nЧтобы посмотреть информацию о всех доступных валютах, введите команду /values\nЕсли хотите посмотреть курс определённой валюты, введите данные в формате <код валюты, цену которой хотите узнать> <код валюты, в которой хотите узнать цену первой валюты> <количество первой валюты>\nПример: EUR RUB 1")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Чтобы посмотреть информацию о всех доступных валютах, введите команду /values\nЕсли хотите посмотреть курс определённой валюты, введите данные в формате <код валюты, цену которой хотите узнать> <код валюты, в которой хотите узнать цену первой валюты> <количество первой валюты>\nПример: EUR RUB 1" )

@bot.message_handler(commands=['values'])
def values(message):
    text = "Доступные валюты:\n"
    for key,val in keys.items():
        text = text + key + " - " + val + "\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def convert(message):
        values, error = currencychecking.convert(message)
        if type(error) == keyisnotexist:
            bot.send_message(message.chat.id,f"Ошибка со стороны пользователя!\nДанной валюты {values} не существует! Введите данные в корректном формате: <код валюты, цену которой хотите узнать> <код валюты, в которой хотите узнать цену первой валюты> <количество первой валюты>\nПример: EUR RUB 1\nПосмотреть список всех доступных валют можно с помощью команды /values")
        elif type(error) == countofvalues:
            bot.send_message(message.chat.id,"Ошибка со стороны пользователя!\nКоличество данных больше или меньше, чем 3!\nВведите данные в корректном формате: <код валюты, цену которой хотите узнать> <код валюты, в которой хотите узнать цену первой валюты> <количество первой валюты>\nПример: EUR RUB 1")
        elif type(error) == equalvalues:
            bot.send_message(message.chat.id, "Ошибка со стороны пользователя!\nНельзя конвертировать одну и ту же валюту!\nВведите данные в корректном формате: <код валюты, цену которой хотите узнать> <код валюты, в которой хотите узнать цену первой валюты> <количество первой валюты>\nПример: EUR RUB 1")
        elif type(error) == ValueError:
            bot.send_message(message.chat.id, "Ошибка со стороны пользователя!\nНе удалось обработать количество валюты!\nВведите данные в корректном формате: <код валюты, цену которой хотите узнать> <код валюты, в которой хотите узнать цену первой валюты> <количество первой валюты>\nПример: EUR RUB 1")
        else:
            text = API.get_price(values)
            if type(text)!=str:
                bot.reply_to(message, f"Ошибка со стороны сервера!\n{text}")
            else:
                bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)