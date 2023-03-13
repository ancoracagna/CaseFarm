import time
from Modules import add_bot, get_list_bots
from settings import API_KEY
import telebot
import sqlite3

bot = telebot.TeleBot(API_KEY)



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
            bot.reply_to(message,str(message.from_user.first_name)+', мы скучали! \nВозвращаем Вас в главное меню!')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)