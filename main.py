import time
from settings import API_KEY
import telebot
import sqlite3

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    try:
        user = message.from_user.id
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE telegram_id LIKE " + str(user))
        results = cursor.fetchall()
        if (len(results) == 0):
            print("User not found")
            cursor.execute("SELECT MAX(id) FROM users")
            result = cursor.fetchall()
            for row in result:
                max = int(row[0]) + 1
            cursor.execute(
                "insert into users values (" + str(max) + ", '" + str(user)+"', '') ")
            conn.commit()
            bot.reply_to(message,'Приветствуем Вас в нашей команде GENESIS, '+str(message.from_user.first_name)+'! \nНам очень приятно что нас становится все больше!\nПозвольте предложить Вам пройти обучение')
        if (len(results) > 0):
            print("User already in system")
            bot.reply_to(message,str(message.from_user.first_name)+', мы скучали! \nВозвращаем Вас в главное меню!')  # добавить выбор клавы по тарифу функцией getkeys() или подобной
    except:
        pass

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)