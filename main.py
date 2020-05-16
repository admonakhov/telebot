import config
import telebot
import re
import time
import myplot
import mymath

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)
bot.send_message(config.OWNER, 'I\'m alive!!!')


def log(message, text=''):
    with open('visitors.txt', 'a') as visit:
        user = str(message.from_user.first_name + ' ' + message.from_user.last_name + ' ' + str(message.chat.id))
        visit.write(
            str((time.ctime()) + ' ' + user + ': ' + ' '.join(re.findall(r"(?:/)(.*)", message.text)) + text + '\n'))


@bot.message_handler(commands=['start'])
def start(message):
    log(message)
    help_key = telebot.types.ReplyKeyboardMarkup(True, True)
    help_b = telebot.types.InlineKeyboardButton("/help")
    help_key.add(help_b)
    user = str(message.from_user.first_name + ' ' + message.from_user.last_name)
    send_mess = "Привет " + user + "!"
    bot.send_message(message.chat.id, send_mess)
    bot.send_message(message.chat.id, "Если нужна помощь - просто нажми...", reply_markup=help_key)


@bot.message_handler(commands=['median', 'mean', 'sko', 'cv', 'sum'])
def calc(msg):
    text = (re.findall(r'(\-*\w+\.*\w*)(?:\s+)*', msg.text))
    cmd = (text.pop(0))
    if len(text) == 0:
        send_mess = 'Чтобы воспользоваться коммандой {0} укажите после нее набор чисел'.format(cmd)
        bot.send_message(msg.chat.id, send_mess)
    else:
        if True not in (list(map(str.isalpha, text))):
            d = list(map(float, text))
            if cmd == 'median':
                bot.send_message(msg.chat.id, "Медиана: {0}".format(str(mymath.median(d))))
            if cmd == 'mean':
                bot.send_message(msg.chat.id, "Среднее значение: {0}".format(str(mymath.mean(d))))
            if cmd == 'sko':
                bot.send_message(msg.chat.id, "СКО: {0}".format(str(mymath.sko(d))))
            if cmd == 'cv':
                bot.send_message(msg.chat.id, "CV: {0} %".format(str(mymath.cv(d))))
            if cmd == 'sum':
                bot.send_message(msg.chat.id, "Сумма: {0}".format(str(sum(d))))


@bot.message_handler(commands=['who'])
def who(message):
    if message.chat.id == config.OWNER:
        with open('visitors.txt') as visitors:
            for line in visitors:
                bot.send_message(config.OWNER, line)
    else:
        bot.send_message(config.OWNER, message.from_user.first_name + ' ' \
                         + message.from_user.last_name + ' ' + 'tr'
                                                               'y to command')
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
    example_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    example_button = telebot.types.InlineKeyboardButton(text='1 -2 3.14')
    example_cmd_button = telebot.types.InlineKeyboardButton(text='/mean 1 -2 3.14')
    cmd_button = telebot.types.InlineKeyboardButton(text='/commands')
    example_keyboard.add(example_button, example_cmd_button, cmd_button)
    bot.send_message(message.chat.id, 'Напишите выборку чисел, чтобы посчитать стандартные статистические параметры,\
                                      если требуется конкретный парметр, укажите его команду, согласно примеру ниже,\
                                      чтобы ознакомиться со списком команд, нажмите соответствующую кнопку:')
    bot.send_message(message.chat.id, 'Например', reply_markup=example_keyboard)
    log(message)


@bot.message_handler(commands=['commands'])
def cmd(msg):
    bot.send_message(msg.chat.id, "/median - медиана \n/mean - среднее \n/sko - СКО \n/cv - коэффициент вариации "
                                  "\n/sum - сумма\n/plot - для построения графика")


@bot.message_handler(commands=['plot'])
def plot(msg):
    helboard = telebot.types.ReplyKeyboardMarkup(True, True)
    helpbutton = telebot.types.KeyboardButton('/plot 5:1 4:2 3:3 2:4')
    helboard.add(helpbutton)
    text = msg.text
    if len(re.findall(r'\s*\d+\s*:\s*\d+\s*', text)) == 0:
        send_mess = 'Чтобы воспользоваться коммандой /plot укажите после нее набор чисел'
        bot.send_message(msg.chat.id, send_mess, reply_markup=helboard)
    else:
        patY = r'\s*(\d+)\s*:'
        patX = r':\s*(\d+)\s*'
        try:
            Y = list(map(float, re.findall(patY, text)))
            X = list(map(float, re.findall(patX, text)))
            myplot.plot(X, Y)
            img = open('tmp.png', 'rb')
            bot.send_photo(msg.chat.id, img)
            img.close()
        except:
            bot.send_message(msg.chat.id, "Что-то не так! Провертье формат записи Y:X", reply_markup=helboard)


@bot.message_handler(content_types=['text'])
def any_text(msg):
    cmd = (re.findall(r'(\-*\w+\.*\w*)(?:\s+)*', msg.text))
    if True not in (list(map(str.isalpha, cmd))):
        d = list(map(float, cmd))
        bot.send_message(msg.chat.id, 'N : {0}'.format(str(len(d))))
        bot.send_message(msg.chat.id, 'Среднее значение: {0}'.format(str(mymath.mean(d))))
        bot.send_message(msg.chat.id, 'СКО: {0}'.format(str(mymath.sko(d))))
        bot.send_message(msg.chat.id, "Коэффициент вариации: {0} %".format(str(mymath.cv(d))))
        bot.send_message(msg.chat.id, "Медиана: {0}".format(str(mymath.median(d))))


while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(e.args)
        time.sleep(2)
