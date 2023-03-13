import sqlite3

def add_bot(message):
    telegram_id = message.from_user.id;
    bot_name = message.text;
    conn = sqlite3.connect('DB/main.db')
    cursor = conn.cursor()
    cursor.execute("SELECT bots FROM users WHERE telegram_id LIKE '" + str(telegram_id) + "'")
    results = cursor.fetchall()
    for row in results:
        try:
            bots = row[0]
        except:
            bots = bot_name
    new_bots = str(bots) +";" + str(bot_name)
    cursor.execute(
        "UPDATE users SET bots = '" + str(new_bots) + "' WHERE telegram_id LIKE '" + str(telegram_id) + "'")
    conn.commit()
    conn.close()

def get_list_bots(user):
    list_bots = []
    conn = sqlite3.connect('DB/main.db')
    cursor = conn.cursor()
    cursor.execute("SELECT bots FROM users WHERE telegram_id LIKE '" + str(user) + "'")
    results = cursor.fetchall()
    for row in results:
        try:
            bots = row[0]
        except:
            pass
    if len(bots)>=1:
        bots = bots[1:]
    list_bots = bots.split(sep=';')
    return list_bots