import config
import telebot
import weather
import re
import time
from telebot import apihelper
from translit import transliterate

#apihelper.proxy = {'https': config.PROXY}
bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

bot.send_message(config.OWNER, 'I\'m alive!!!')
keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row('weather Moscow', 'weather Saint Petersburg', 'weather Vladimir')



def log(message, text=''):
    with open('visitors.txt', 'a') as visit:
        user = str(message.from_user.first_name + ' ' + message.from_user.last_name + ' ' + str(message.chat.id))
        visit.write(str((time.ctime()) + ' ' + user + ': ' + ' '.join(re.findall(r"(?:/)(.*)", message.text)) + text + '\n'))


@bot.message_handler(commands=['start'])
def start(message):
    log(message)
    user = str(message.from_user.first_name + ' ' + message.from_user.last_name)
    send_mess = "Hello " + user + ' would you like to know a /weather'
    bot.send_message(message.chat.id, send_mess, reply_markup=keyboard)


@bot.message_handler(commands=['weather', 'погода'])
def _weather(message):
    city = transliterate(''.join(re.findall(r"(?:weather *|погода *)([\w, \-]*)", message.text)).lower())
    log(message)
    if city:
        try:
            w = weather.weather(city)
        except Exception as E:
            log(message,' '.join(E.__str__()))
            bot.send_message(message.chat.id, "Bad city's name, probaly...")
            w = weather.weather()
    else:
        w = weather.weather()
    bot.send_message(message.chat.id, "Temperature in " + weather._city + ' is ' + str(w['temp']) + ' C')
    bot.send_message(message.chat.id, "Feels like " + str(w['feels_like']) + ' C')
    bot.send_message(message.chat.id, "Pressure is  " + str(w['pressure']) + ' kPa')
    bot.send_message(message.chat.id, "Humidity is  " + str(w['humidity']) + ' %')


@bot.message_handler(commands=['who'])
def who(message):
    print('work2')
    if message.chat.id == config.OWNER:
        with open('visitors.txt') as visitors:
            for line in visitors:
                bot.send_message(config.OWNER, line)
    else:
        bot.send_message(config.OWNER, message.from_user.first_name + ' ' \
                         + message.from_user.last_name + ' ' + 'try to command')
        bot.send_message(message.chat.id, "You have not permission, you will reported")
        log(message)


@bot.message_handler(commands=['clear'])
def clear(message):
    if message.chat.id == config.OWNER:
        with open('visitors.txt', 'w') as visitors:
            bot.send_message(config.OWNER, 'the log has been cleared')
    else:
        bot.send_message(config.OWNER, message.from_user.first_name + ' ' \
                         + message.from_user.last_name + ' ' + 'try to command')
        bot.send_message(message.chat.id, "You have not permission, you will reported")
        log(message)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'You can write /weather city to see weather in any city')
    bot.send_message(message.chat.id, 'If you are a moderator you may use /who to see visitor\'s list and /clear this list,\
    in any case you will reported')
    log(message)


@bot.message_handler(content_types=['text'])
def any_text(msg):
    cmd = ''.join(re.findall(r'(\w+\b)(?:.*)', msg.text)).lower()
    if cmd in ['погода', 'weather']:
        _weather(msg)
    else:
        bot.send_message(msg.chat.id, 'I can\'t understand what you mean')
        help(msg)


while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(e.args)
        time.sleep(2)
