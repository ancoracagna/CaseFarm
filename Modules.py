import sqlite3, telebot

def show_keys():
    kb = telebot.types.InlineKeyboardMarkup()
    kb.add(telebot.types.InlineKeyboardButton(text='Recoil Case', callback_data='Recoil_Case'))
    kb.add(telebot.types.InlineKeyboardButton(text='Snakebite Case', callback_data='Snakebite_Case'))
    kb.add(telebot.types.InlineKeyboardButton(text='Fracture Case', callback_data='Fracture_Case'))
    kb.add(telebot.types.InlineKeyboardButton(text='Dreams & Nightmares Case', callback_data='Dreams_Nightmares_Case'))
    kb.add(telebot.types.InlineKeyboardButton(text='Clutch Case', callback_data='Clutch_Case'))
    kb.add(telebot.types.InlineKeyboardButton(text='Revolution Case', callback_data='Revolution_Case'))
    return kb

def add_casetobot(message):
    bot_name = message.text;
    kb = telebot.types.InlineKeyboardMarkup()
    kb.add(telebot.types.InlineKeyboardButton(text='Recoil Case', callback_data='Recoil_Case'+'|'+str(bot_name)))
    kb.add(telebot.types.InlineKeyboardButton(text='Snakebite Case', callback_data='Snakebite_Case'+'|'+str(bot_name)))
    kb.add(telebot.types.InlineKeyboardButton(text='Fracture Case', callback_data='Fracture_Case'+'|'+str(bot_name)))
    kb.add(telebot.types.InlineKeyboardButton(text='Dreams & Nightmares Case', callback_data='Dreams_Nightmares_Case'+'|'+str(bot_name)))
    kb.add(telebot.types.InlineKeyboardButton(text='Clutch Case', callback_data='Clutch_Case'+'|'+str(bot_name)))
    kb.add(telebot.types.InlineKeyboardButton(text='Revolution Case', callback_data='Revolution_Case'+'|'+str(bot_name)))
    return kb

def get_bot_cases(bot_name):
    cases = []
    try:
        conn = sqlite3.connect('DB/main.db')
        cursor = conn.cursor()
        cursor.execute("SELECT cases FROM bots WHERE bot_name LIKE '" + str(bot_name) + "'")
        results = cursor.fetchall()
        for row in results:
            try:
                cases = row[0]
            except:
                bots = bot_name
        conn.close()
        cases_str = str(cases)
        cases = cases_str.split(',')
    except:
        print('Не удалось получить кейсы по пользователю')
    return cases

def get_case_cost(case):
    case_cost = 0
    try:
        conn = sqlite3.connect('DB/main.db')
        cursor = conn.cursor()
        case = case[1:]
        print('CaseName: '+str(case))
        cursor.execute("SELECT case_cost FROM cases WHERE case_name LIKE '" + str(case) + "'")
        results = cursor.fetchall()
        for row in results:
            try:
                case_cost = int(row[0])
            except:
                print('error')
    except:
        case_cost = 0
    return case_cost

def get_summary(cases):
    summ = 0
    for case in cases:
        cost = get_case_cost(case)
        summ+=cost
    return summ
def add_casedrop(bot_name, case):
    try:
        conn = sqlite3.connect('DB/main.db')
        cursor = conn.cursor()
        cursor.execute("SELECT cases FROM bots WHERE bot_name LIKE '" + str(bot_name) + "'")
        results = cursor.fetchall()
        for row in results:
            try:
                cases = row[0]
            except:
                bots = bot_name
        cases_new = str(cases) + ', '+str(case)
        cursor.execute("UPDATE bots SET cases = '" + str(cases_new) + "' WHERE bot_name LIKE '" + str(bot_name) + "'")
        conn.commit()
        conn.close()
    except:
        print('Не удалось добавить кейс')

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
    cursor.execute("SELECT MAX(id) FROM bots")
    result = cursor.fetchall()
    for row in result:
        max = int(row[0]) + 1
    cursor.execute("insert into bots values (" + str(max) + ", '" + str(bot_name) + "', '0') ")
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