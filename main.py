import time
from Modules import add_bot, get_list_bots, show_keys, add_casedrop
from Keyboard import initk
from settings import API_KEY
import telebot
import sqlite3

bot = telebot.TeleBot(API_KEY)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if 'Case' in call.data:
        case, bot_name = str(call.data).split('|')
        add_casedrop(bot_name, case)

@bot.message_handler(regexp='Добавить дроп')
def handle(msg):
    bot.send_message(msg.from_user.id, 'Напишите ник бота которого необходимо добавить: ')
    bot.register_next_step_handler(msg, add_casetobot);

def add_casetobot(message):
    bot_name = message.text;
    kb = telebot.types.InlineKeyboardMarkup()
    kb.add(telebot.types.InlineKeyboardButton(text='Recoil Case', callback_data='Recoil_Case'+'|'+str(bot_name)))
    kb.add(telebot.types.InlineKeyboardButton(text='Snakebite Case', callback_data='Snakebite_Case'+'|'+str(bot_name)))
    kb.add(telebot.types.InlineKeyboardButton(text='Fracture Case', callback_data='Fracture_Case'+'|'+str(bot_name)))
    kb.add(telebot.types.InlineKeyboardButton(text='Dreams & Nightmares Case', callback_data='Dreams_Nightmares_Case'+'|'+str(bot_name)))
    kb.add(telebot.types.InlineKeyboardButton(text='Clutch Case', callback_data='Clutch_Case'+'|'+str(bot_name)))
    kb.add(telebot.types.InlineKeyboardButton(text='Revolution Case', callback_data='Revolution_Case'+'|'+str(bot_name)))
    bot.send_message(message.from_user.id, 'Клавиатура: ',reply_markup=kb)

@bot.message_handler(regexp='Добавить бота')
def handle(msg):
    bot.send_message(msg.from_user.id, 'Напишите ник бота которого необходимо добавить: ')
    bot.register_next_step_handler(msg, add_bot);

@bot.message_handler(regexp='Мои боты')
def handle(msg):
    list_bots = get_list_bots(msg.from_user.id)
    bots = ''
    for bot_name in list_bots:
        bots = bots + '\n🔸 '+ str(bot_name)+ ': '+' кейсов, на сумму: '+' рублей'
    text = 'Список Ваших ботов: \n'+ str(bots)+'\n\nСтатистика на '+'_ число'
    bot.send_message(msg.from_user.id, str(text))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    try:
        user = message.from_user.id
        conn = sqlite3.connect('DB/main.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE telegram_id LIKE " + str(user))
        results = cursor.fetchall()
        if (len(results) == 0):
            cursor.execute("SELECT MAX(id) FROM users")
            result = cursor.fetchall()
            for row in result:
                max = int(row[0]) + 1
            cursor.execute("insert into users values (" + str(max) + ", '" + str(user)+"', '') ")
            conn.commit()
            bot.reply_to(message,'Приветствуем Вас в нашей команде GENESIS, '+str(message.from_user.first_name)+'! \nНам очень приятно что нас становится все больше!\nПозвольте предложить Вам пройти обучение')
        if (len(results) > 0):
            bot.reply_to(message,str(message.from_user.first_name)+', мы скучали! \nВозвращаем Вас в главное меню!', reply_markup=main_menu)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main_menu = initk()
    #while True:
    #    try:
    bot.polling(none_stop=True)
    #    except Exception as e:
    #        time.sleep(3)
    #        print(e)