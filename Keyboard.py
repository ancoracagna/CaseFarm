import telebot

def initk():
    main_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu.add('Мои боты')
    main_menu.add('Добавить дроп')
    main_menu.add('Добавить бота')
    return main_menu