import json
from telebot import types

def main_keyboard():
    markup_main = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    button1 = "📝Отрисовка (Чеки, балансы)"
    button2 = "🖼Готовые скрины"
    button3 = "🙋Здесь могла быть твоя реклама!"
    button4 = "👁Информация"
    button5 = "📩Отрисовка писем"
    markup_main.row(button1, button2, button5)
    markup_main.row(button3, button4)
    return markup_main
def back_keyboard_check():
    markup_qiwi_back = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button1 = "Вернуться в Меню🧭"
    button2 = "Ещё раз"
    markup_qiwi_back.row(button2, button1)
    return markup_qiwi_back
def keyboard_qiwi():
    markup_qiwi = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = 'Фейк баланс💰'
    btn2 = 'Фейк чек🧾'
    btn3 = 'Назад'
    markup_qiwi.row(btn1, btn2)
    markup_qiwi.row(btn3)
    return markup_qiwi
def checks_and_balances_keyboard():
    checks_and_balances_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = 'QIWI🐥'
    btn2 = "Тинькофф💛"
    btn3 = 'Назад'
    btn4 = 'Сбер♻️'
    btn5 = 'ПриватБанк🔵'
    checks_and_balances_markup.row(btn1, btn2, btn4)
    checks_and_balances_markup.row(btn5, btn3)
    return checks_and_balances_markup
def tinkoff():
    tinkoff_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = "Тинькофф Перевод"
    btn2 = "💲Оплата Авито"
    btn3 = "Назад"
    btn4 = "🌀Оплата Юла"
    tinkoff_markup.row(btn1)
    tinkoff_markup.row(btn2,btn4)
    tinkoff_markup.row(btn3)
    return tinkoff_markup
def back():
    back_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = 'Назад'
    back_markup.row(btn1)
    return back_markup
def screens():
    screens_markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = '📦Скрины Авито'
    btn2 = '📦Скрины Юла'
    btn3 = 'Назад'
    screens_markup.row(btn1, btn2)
    screens_markup.row(btn3)
    return screens_markup
def sber():
    sber_markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = "♻️Перевод Сбер♻️"
    btn2 = "Назад"
    sber_markup.row(btn1, btn2)
    return sber_markup
def admin():
    admin_markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = "Сделать рассылку"
    btn2 = "Выход"
    admin_markup.row(btn1, btn2)
    return admin_markup
def rassilka_keyboard():
    rassilka_markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = "Отменить"
    rassilka_markup.row(btn1)
    return rassilka_markup
def mail():
    mail_markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = "Письмо Avito"
    btn2 = "Письмо Юла"
    btn3 = "Назад"
    mail_markup.row(btn1, btn2)
    mail_markup.row(btn3)
    return mail_markup