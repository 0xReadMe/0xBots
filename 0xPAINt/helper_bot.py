import telebot
from keyboard import main_keyboard, back_keyboard_check, keyboard_qiwi, checks_and_balances_keyboard, back, tinkoff, screens, sber, admin, rassilka_keyboard, mail
from telebot.types import InputMediaPhoto
import sqlite3
from PIL import Image, ImageFont, ImageDraw
import json
import random
import os
import time
from telebot import types
global ADMIN_ID
ADMIN_ID =  #Сюда свой айди

token = '' #Токен бота

bot = telebot.AsyncTeleBot(token)

@bot.message_handler(commands=['start']) #Авторизация пользователей, выдача кол-ва пользователей админу.
def start_message(message):
    con = sqlite3.connect('counter.db')
    cur = con.cursor()
    db = sqlite3.connect('users.db')
    sql = db.cursor()

    sql.execute("""CREATE TABLE IF NOT EXISTS users (
        id INT
    )""")
    
    con.commit()
    db.commit()
    id = message.chat.id
    sql.execute(f"SELECT id FROM users WHERE id = '{id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES (?)", (id,))
        cur.execute(f"SELECT count FROM counter")
        c = cur.fetchone()[0] + 1
        print(c)
        cur.execute(f"UPDATE counter SET count = {c}")
        bot.send_message(message.chat.id, '🧾Привет! У меня ты сможешь сделать фейк чеки популярных приложений. Надеюсь тебе понравится :)\n⚠️Воспользуйся кнопками для управления ботом\nПо всем вопросам: @slivmens', reply_markup=main_keyboard())
        db.commit()
        con.commit()
    else: 
        bot.send_message(message.chat.id, '🧾Привет, у меня ты сможешь сделать фейк чеки популярных приложений. Надеюсь тебе понравится :)\n⚠️Воспользуйся кнопками для управления ботом\nПо всем вопросам: @slivmens', reply_markup=main_keyboard())
   
@bot.message_handler(content_types="text") #Работа бота
def main(message):
    if message.text == '📝Отрисовка (Чеки, балансы)':
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=checks_and_balances_keyboard())
        bot.register_next_step_handler(message, checks_and_balances)
    elif message.text == "🖼Готовые скрины":
        bot.send_message(message.chat.id, 'Готовые чеки, выберите категорию:',reply_markup=screens())
        bot.register_next_step_handler(message, screen)
    elif message.text == "👁Информация":
        con = sqlite3.connect('counter.db')
        cur = con.cursor()
        cur.execute("SELECT count FROM counter")
        count = cur.fetchone()[0]        
        bot.send_message(message.chat.id, f"👁Информация\n\nВаш id: {message.chat.id}\nАдмин Бота: @slivmens\n\nПользователей в Боте: {count}", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    elif message.text == "Админ" and message.chat.id == ADMIN_ID:        
        bot.send_message(message.chat.id, "Вы перещли в меню админа", reply_markup=admin())
        bot.register_next_step_handler(message, admin_panel)
    elif message.text == "🙋Здесь могла быть твоя реклама!":
        bot.send_message(message.chat.id, "Заказать рекламу: @slivmens", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    elif message.text == "📩Отрисовка писем":
        bot.send_message(message.chat.id, "Выберите категорию: ", reply_markup=mail())
        bot.register_next_step_handler(message, mail_)
    elif message.text == "Нaзад":
        bot.send_message(message.chat.id, "Выберите категорию: ")
        bot.register_next_step_handler(message, mail_)
    else:
        bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
def mail_(message):
    if message.text == "Письмо Avito":
        bot.send_message(message.chat.id, "Введите текст письма: ", reply_markup=back())
        bot.register_next_step_handler(message, mail_avito)
    elif message.text == "Письмо Юла":
        bot.send_message(message.chat.id, "Введите текст письма: ", reply_markup=back())
        bot.register_next_step_handler(message, mail_youla)
    elif message.text == "Назад":
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
def mail_avito(message):
    if message.text == "Назад":       
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    else:
        if message.text:
            if message.text == "Вернуться в Меню🧭":
                bot.send_message(message.chat.id, "Выберите категорию из списка:", reply_markup=main_keyboard())
                bot.register_next_step_handler(message, main)
            elif message.text == "Ещё раз":
                bot.send_message(message.chat.id, "Введите текст письма: ")
                bot.register_next_step_handler(message, mail_avito)
            else:
                try:
                    text = message.text
                    tink = Image.open('Image source/mail_avito.png')
                    font = ImageFont.truetype('Fonts/arial.ttf', 22)
                    d = ImageDraw.Draw(tink)
                    d.text((26,486), text, font=font, fill=(0, 0, 0,255))
                    tink.save("Image cache/file3.png", "PNG")
                    img = open('Image cache/file3.png', 'rb')
                    bot.send_photo(message.chat.id, img, reply_markup=back_keyboard_check())
                    bot.register_next_step_handler(message, mail_avito)
                except Exception as ex:
                    print(ex)
                    bot.send_message(message.chat.id, 'Что-то пошло не так. Возврат в меню..', reply_markup=main_keyboard())
                    bot.register_next_step_handler(message, main)
        else:
            bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
            bot.register_next_step_handler(message, main)
def mail_youla(message):
    if message.text == "Назад":       
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    else:
        if message.text:
            if message.text == "Вернуться в Меню🧭":
                bot.send_message(message.chat.id, "Выберите категорию из списка:", reply_markup=main_keyboard())
                bot.register_next_step_handler(message, main)
            elif message.text == "Ещё раз":
                bot.send_message(message.chat.id, "Введите текст письма: ")
                bot.register_next_step_handler(message, mail_youla)
            else:
                try:
                    text = message.text
                    tink = Image.open('Image source/mail_youla.png')
                    font = ImageFont.truetype('Fonts/arial.ttf', 22)
                    d = ImageDraw.Draw(tink)
                    d.text((26,486), text, font=font, fill=(0, 0, 0,255))
                    tink.save("Image cache/file3.png", "PNG")
                    img = open('Image cache/file3.png', 'rb')
                    bot.send_photo(message.chat.id, img, reply_markup=back_keyboard_check())
                    bot.register_next_step_handler(message, mail_youla)
                except Exception as ex:
                    print(ex)
                    bot.send_message(message.chat.id, 'Что-то пошло не так. Возврат в меню..', reply_markup=main_keyboard())
                    bot.register_next_step_handler(message, main)
        else:
            bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
            bot.register_next_step_handler(message, main)
        
def admin_panel(message):
    if message.text == "Сделать рассылку" and message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Введите текст рассылки: ", reply_markup=rassilka_keyboard())
        bot.register_next_step_handler(message, rassilka)
    elif message.text == "Выход" and message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Выход из панели админа", reply_message=main_keyboard())
        bot.register_next_step_handler(message, main)
def rassilka(message):
    if message.text == "Отменить" and message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Отменено", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    elif message.text and message.chat.id == ADMIN_ID:
        text = message.text
        db = sqlite3.connect('users.db')
        sql = db.cursor()
        sql.execute("SELECT id FROM users")
        id = sql.fetchall()
        for id in id:
            for id in id:
               try:
                bot.send_message(id, f"{text}")
                time.sleep(1)
               except:
                   sql.execute(f"DELETE FROM users WHERE id = {id}")
        bot.send_message(ADMIN_ID, "Рассылка завершена", reply_markup=main_keyboard())
        db.commit()
        bot.register_next_step_handler(message, main)

def screen(message):
    if message.text == "📦Скрины Авито":
        a1 = open('Screens/a1.jpg', 'rb')
        a2 = open('Screens/a2.jpg', 'rb')
        a3 = open('Screens/a3.jpg', 'rb')
        a4 = open('Screens/a4.jpg', 'rb')
        a5 = open('Screens/a5.jpg', 'rb')
        bot.send_media_group(message.chat.id, [InputMediaPhoto(a1),InputMediaPhoto(a2), InputMediaPhoto(a3), InputMediaPhoto(a4),InputMediaPhoto(a5)])
        bot.register_next_step_handler(message, screen)
    elif message.text == "📦Скрины Юла":
        y1 = open('Screens/y1.jpg', 'rb')
        y2 = open('Screens/y2.jpg', 'rb')
        y3 = open('Screens/y3.jpg', 'rb')
        y4 = open('Screens/y4.jpg', 'rb')
        y5 = open('Screens/y5.jpg', 'rb')
        bot.send_media_group(message.chat.id, [InputMediaPhoto(y1),InputMediaPhoto(y2), InputMediaPhoto(y3), InputMediaPhoto(y4),InputMediaPhoto(y5)])
        bot.register_next_step_handler(message, screen)
    elif message.text == "Назад":
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    else:
        bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
def checks_and_balances(message):
    if message.text == "Тинькофф💛":
        bot.send_message(message.chat.id, '💛Доступные чеки Тинькофф:', reply_markup=tinkoff())
        bot.register_next_step_handler(message, tinkov)
    elif message.text == 'Сбер♻️':
        bot.send_message(message.chat.id, "♻️Сбер, Доступные чеки:", reply_markup=sber())
        bot.register_next_step_handler(message, sber_menu)
    elif message.text == 'QIWI🐥':
        bot.send_message(message.chat.id, '🐥Вы выбрали QIWI. \n Выберите категорию:', reply_markup=keyboard_qiwi())
        bot.register_next_step_handler(message, qiwi)
    elif message.text == "Назад":
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    elif message.text == 'ПриватБанк🔵':
        bot.send_message(message.chat.id, "OLX Приватбанк, заполните форму: \n\nСистемное время\nДата и время\nСумма перевода\nОстаток \n\n❗️Разделяйте параметры переносом строки❗️", reply_markup=back())
        bot.register_next_step_handler(message, privat)
    else:
        bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
def privat(message):
    if message.text == "Назад":       
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    else:
        if message.text:
            if message.text == "Вернуться в Меню🧭":
                bot.send_message(message.chat.id, "Выберите категорию из списка:", reply_markup=main_keyboard())
                bot.register_next_step_handler(message, main)
            elif message.text == "Ещё раз":
                bot.send_message(message.chat.id, "OLX Приватбанк, заполните форму: \n\nСистемное время\nДата и время\nСумма перевода\nОстаток \n\n❗️Разделяйте параметры переносом строки❗️")
                bot.register_next_step_handler(message, privat)
            else:
                try:
                    text = message.text.split("\n")
                    time = text[0]
                    date_time = text[1]
                    money = "-"+text[2]+" ГРН"
                    balance = text[3] + " ГРН"
                    tink = Image.open('Image source/privatbank.png')
                    font_time = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 37)
                    font_date_time = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 43)
                    font_money = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 80)
                    font_balance = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 57)
                    w1, h1 = font_money.getsize(money)
                    w2, h2 = font_balance.getsize(balance)
                    W = 1080
                    d = ImageDraw.Draw(tink)
                    d.text((945,45), time, font=font_time, fill=(228, 255, 194, 255))
                    d.text((51, 420), date_time, font=font_date_time, fill=(102, 102, 102,255))
                    d.text(((W - w1)/2,540), money, font=font_money, fill=(0,0,0,255))
                    d.text(((W - w2)/2, 1060), balance, font=font_balance, fill=(0,0,0,255))
                    tink.save("Image cache/file3.png", "PNG")
                    img = open('Image cache/file3.png', 'rb')
                    bot.send_photo(message.chat.id, img, reply_markup=back_keyboard_check())
                    bot.register_next_step_handler(message, sber_transfer)
                except Exception as ex:
                    print(ex)
                    bot.send_message(message.chat.id, 'Что-то пошло не так. Возврат в меню..', reply_markup=main_keyboard())
                    bot.register_next_step_handler(message, main)
        else:
            bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
            bot.register_next_step_handler(message, main)
def sber_menu(message):
    if message.text == "♻️Перевод Сбер♻️":
        photo = open('Image reference/sber_transfer.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption="Пример перевода")
        time.sleep(0.2)
        bot.send_message(message.chat.id, "♻️Выбран перевод сбер. Заполните форму:\n\nСистемное время\nИмя получателя\nСумма \n\n❗️Разделяйте параметры переносом строки❗️")
        bot.register_next_step_handler(message, sber_transfer)
    elif message.text == "Назад":
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    else:
        bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
def sber_transfer(message):
    if message.text == "Назад":       
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    else:
        if message.text:
            if message.text == "Вернуться в Меню🧭":
                bot.send_message(message.chat.id, "Выберите категорию из списка:", reply_markup=main_keyboard())
                bot.register_next_step_handler(message, main)
            elif message.text == "Ещё раз":
                bot.send_message(message.chat.id, "♻️Выбран перевод сбер. Заполните форму:\n\nСистемное время\nИмя получателя\nСумма \n\n❗️Разделяйте параметры переносом строки❗️")
                bot.register_next_step_handler(message, sber_transfer)
            else:
                try:
                    text = message.text.split("\n")
                    time = text[0]
                    name = text[1]
                    money = text[2]+" ₽"
                    tink = Image.open('Image source/sber_transfer.png')
                    font_time = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 39)
                    font_name = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 43)
                    font_money = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 80)
                    d = ImageDraw.Draw(tink)
                    d.text((70,25), time, font=font_time, fill=(225, 238, 229,255))
                    d.text((200,245), name, font=font_name, fill=(255,255,255,255))
                    d.text((200, 325), money, font=font_money, fill=(255,255,255,255))
                    tink.save("Image cache/file3.png", "PNG")
                    img = open('Image cache/file3.png', 'rb')
                    bot.send_photo(message.chat.id, img, reply_markup=back_keyboard_check())
                    bot.register_next_step_handler(message, sber_transfer)
                except Exception as ex:
                    print(ex)
                    bot.send_message(message.chat.id, 'Что-то пошло не так. Возврат в меню..', reply_markup=main_keyboard())
                    bot.register_next_step_handler(message, main)
        else:
            bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
            bot.register_next_step_handler(message, main)
        

def tinkov(message):
    if message.text == "Тинькофф Перевод":
        photo = open('Image reference/tinkoff_transfer.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption="Пример перевода")
        time.sleep(0.1)
        bot.send_message(message.chat.id, "Тинькофф перевод, заполните форму:\n\nСистемное время\nДата и время платежа\nСумма(только Рубли и копейки, остальное поставится за вас. Например 1500,00)\nНа карту\n\n❗️Разделяйте параметры переносом строки❗️",reply_markup=back())
        bot.register_next_step_handler(message, tinkov_tranfer)
    elif message.text == "Назад":
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    elif message.text == "💲Оплата Авито":
        photo = open('Image reference/tinkoff_avito.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption="Пример оплаты")
        time.sleep(0.1)
        bot.send_message(message.chat.id, "Тинькофф оплата Авито, заполните форму:\n\nСистемное время\nДата и время платежа\nСумма(только Рубли и копейки, остальное поставится за вас. Например 1500,00)\nПоследние 4 цифры вашей карты\nКэшбэк\n\n❗️Разделяйте параметры переносом строки❗️",reply_markup=back())
        bot.register_next_step_handler(message, tinkov_avito)
    elif message.text == "🌀Оплата Юла":
        photo = open('Image reference/tinkoff_youla.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption="Пример оплаты")
        time.sleep(0.1)
        bot.send_message(message.chat.id, "Тинькофф оплата Юла, заполните форму:\n\nСистемное время\nДата и время платежа\nСумма(только Рубли и копейки, остальное поставится за вас. Например 1500,00)\nПоследние 4 цифры вашей карты\nКэшбэк\n\n❗️Разделяйте параметры переносом строки❗️",reply_markup=back())
        bot.register_next_step_handler(message, tinkov_youla)
    else:
        bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
def tinkov_youla(message):
    if message.text == "Назад":     
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    else:
        if message.text:
            if message.text == "Вернуться в Меню🧭":
                bot.send_message(message.chat.id, "Выберите категорию из списка:", reply_markup=main_keyboard())
                bot.register_next_step_handler(message, main)
            elif message.text == "Ещё раз":
                bot.send_message(message.chat.id, "Тинькофф оплата Юла, заполните форму:\n\nСистемное время\nДата и время платежа\nСумма(только Рубли и копейки, остальное поставится за вас. Например 1500,00)\nПоследние 4 цифры вашей карты\nКэшбэк\n\n❗️Разделяйте параметры переносом строки❗️")
                bot.register_next_step_handler(message, tinkov_youla)
            else:
                try:
                    text = message.text.split("\n")
                    time = text[0]
                    date_time = text[1]
                    money = "– "+text[2]+"₽"
                    rec = "Tinkoff Black *"+text[3]
                    cashback = "+"+text[4]+" ₽"
                    tink = Image.open('Image source/tinkoff_youla_pay.png')
                    font_time = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 39)
                    font_date_time = ImageFont.truetype('Fonts/Roboto-Medium.ttf', 53)
                    font_money = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 90)
                    font_rec = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 45)
                    W = 1080
                    w1, h1 = font_time.getsize(money)
                    w2, h2 = font_time.getsize(cashback)
                    d = ImageDraw.Draw(tink)
                    d.text((70,25), time, font=font_time, fill=(195,195,195,255))
                    d.text((193,125), date_time, font=font_date_time, fill=(255,255,255,255))
                    d.text(((W - w1-260)/2, 755), money, font=font_money, fill=(255,255,255,255))
                    d.text(((W-44-w2),1861), cashback, font=font_rec, fill=(255,255,255,255))
                    d.text((190,1525), rec, font=font_rec, fill=(255,255,255,255))
                    tink.save("Image cache/file3.png", "PNG")
                    img = open('Image cache/file3.png', 'rb')
                    bot.send_photo(message.chat.id, img, reply_markup=back_keyboard_check())
                    bot.register_next_step_handler(message, tinkov_youla)
                except Exception as ex:
                    print(ex)
                    bot.send_message(message.chat.id, 'Что-то пошло не так. Возврат в меню..', reply_markup=main_keyboard())
                    bot.register_next_step_handler(message, main)
        else:
            bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
            bot.register_next_step_handler(message, main)
def tinkov_avito(message):
    if message.text == "Назад":
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    else:
        if message.text:
            if message.text == "Вернуться в Меню🧭":
                bot.send_message(message.chat.id, "Выберите категорию из списка:", reply_markup=main_keyboard())
                bot.register_next_step_handler(message, main)
            elif message.text == "Ещё раз":
                bot.send_message(message.chat.id, "Тинькофф оплата Авито, заполните форму:\n\nСистемное время\nДата и время платежа\nСумма(только Рубли и копейки, остальное поставится за вас. Например 1500,00)\nПоследние 4 цифры вашей карты\nКэшбэк\n\n❗️Разделяйте параметры переносом строки❗️")
                bot.register_next_step_handler(message, tinkov_avito)
            else:
                try:
                    text = message.text.split("\n")
                    time = text[0]
                    date_time = text[1]
                    money = "– "+text[2]+"₽"
                    rec = "Tinkoff Black *"+text[3]
                    cashback = "+"+text[4]+" ₽"
                    tink = Image.open('Image source/tinkoff_avito_pay.png')
                    font_time = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 39)
                    font_date_time = ImageFont.truetype('Fonts/Roboto-Medium.ttf', 53)
                    font_money = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 90)
                    font_rec = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 45)
                    W = 1080
                    w1, h1 = font_time.getsize(money)
                    w2, h2 = font_time.getsize(cashback)
                    d = ImageDraw.Draw(tink)
                    d.text((70,25), time, font=font_time, fill=(195,195,195,255))
                    d.text((193,125), date_time, font=font_date_time, fill=(255,255,255,255))
                    d.text(((W - w1-260)/2, 755), money, font=font_money, fill=(255,255,255,255))
                    d.text(((W-44-w2),1861), cashback, font=font_rec, fill=(255,255,255,255))
                    d.text((190,1525), rec, font=font_rec, fill=(255,255,255,255))
                    tink.save("Image cache/file3.png", "PNG")
                    img = open('Image cache/file3.png', 'rb')
                    bot.send_photo(message.chat.id, img, reply_markup=back_keyboard_check())
                    bot.register_next_step_handler(message, tinkov_avito)
                except:
                    bot.send_message(message.chat.id, 'Что-то пошло не так. Возврат в меню..', reply_markup=main_keyboard())
                    bot.register_next_step_handler(message, main)
        else:
            bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
            bot.register_next_step_handler(message, main)
def tinkov_tranfer(message):
    if message.text == "Назад":
            bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
            bot.register_next_step_handler(message, main)
    else:
        if message.text:
            if message.text == "Вернуться в Меню🧭":
                bot.send_message(message.chat.id, "Выберите категорию из списка:", reply_markup=main_keyboard())
                bot.register_next_step_handler(message, main)
            elif message.text == "Ещё раз":
                bot.send_message(message.chat.id, "Тинькофф перевод, заполните форму:\n\nСистемное время\nДата и время платежа\nСумма\nНа карту\n\n❗️Разделяйте параметры переносом строки❗️")
                bot.register_next_step_handler(message, tinkov_tranfer)
            else:
                try:
                    text = message.text.split("\n")
                    time = text[0]
                    date_time = text[1]
                    money = "– "+text[2]+"₽"
                    rec = text[3]
                    tink = Image.open('Image source/tinkoff_transfer.png')
                    font_time = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 39)
                    font_date_time = ImageFont.truetype('Fonts/Roboto-Medium.ttf', 53)
                    font_money = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 90)
                    font_rec = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 45)
                    W = 1080
                    w1, h1 = font_time.getsize(money)
                    d = ImageDraw.Draw(tink)
                    d.text((70,25), time, font=font_time, fill=(195,195,195,255))
                    d.text((193,125), date_time, font=font_date_time, fill=(255,255,255,255))
                    d.text(((W - w1-260)/2, 755), money, font=font_money, fill=(255,255,255,255))
                    d.text((45,1878), rec, font=font_rec, fill=(255,255,255,255))
                    tink.save("Image cache/file3.png", "PNG")
                    img = open('Image cache/file3.png', 'rb')
                    bot.send_photo(message.chat.id, img, reply_markup=back_keyboard_check())
                    bot.register_next_step_handler(message, tinkov_tranfer)
                except:
                    bot.send_message(message.chat.id, 'Что-то пошло не так. Возврат в меню..', reply_markup=main_keyboard())
                    bot.register_next_step_handler(message, main)
        else:
            bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
            bot.register_next_step_handler(message, main)
def qiwi(message):
    if message.text == 'Фейк баланс💰':
        photo = open('Image reference/qiwi_balance.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption="Пример оплаты")
        time.sleep(0.1)
        bot.send_message(message.chat.id, "Какой баланс вы хотите?(Например 151,02. Знак ₽ поставится за вас!", reply_markup=back())
        bot.register_next_step_handler(message, qiwi_balance2)
    elif message.text == 'Фейк чек🧾':
        photo = open('Image reference/qiwi_transfer.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption="Пример оплаты")
        time.sleep(0.1)
        bot.send_message(message.chat.id, 'Введите сумму, номер перевода, дату и время в таком формате:\n151,92\n+79XXXXXXXXX\n01.12.2020 в 19:01', reply_markup=back())
        bot.register_next_step_handler(message, qiwi_check)
    elif message.text == "Назад":
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    else:
        bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
def qiwi_check(message):
    
    if message.text:
        
        if message.text == "Назад":
            bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
            bot.register_next_step_handler(message, main)
        else:
            try:
                text = message.text.split("\n")
                money = text[0] + " ₽"
                money2 = "- " + text[0].strip() + " ₽"
                phone = text[1].strip()
                date_time = text[2].strip()
                qiwi = Image.open('Image source/qiwi_check.png')
                font1 = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 53)
                font2 = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 38)
                font3 = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 45)
                font4 = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 45)
                W = 1080
                w1, h1 = font1.getsize(money2)
                w2, h2 = font1.getsize(phone)
                d = ImageDraw.Draw(qiwi)
                d.text(((W-w1)/2,685), money2, font=font1, fill=(0,0,0,255))
                d.text(((W-w2)/2 + 60,614), phone, font=font2, fill=(153,153,153,255))
                d.text((56,1890), date_time, font=font3, fill=(0,0,0,255))
                d.text((56,2072), money, font=font4, fill=(0,0,0,255))
                qiwi.save("Image cache/file3.png", "PNG")
                img = open('Image cache/file3.png', 'rb')
                bot.send_photo(message.chat.id, img, reply_markup=back_keyboard_check())
                bot.register_next_step_handler(message, qiwi_check2)
            except:
                bot.send_message(message.chat.id, 'Что-то пошло не так. Возврат в меню..', reply_markup=main_keyboard())
                bot.register_next_step_handler(message, main)
def qiwi_check2(message):
    if message.text == "Вернуться в Меню🧭":
        bot.send_message(message.chat.id, "Выберите категорию из списка:", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    elif message.text == "Ещё раз":
        bot.send_message(message.chat.id, "Введите сумму, номер перевода, дату и время в таком формате:\n151,92\n+79XXXXXXXXX\n01.12.2020 в 19:01")
        bot.register_next_step_handler(message, qiwi_check)
    else:
        bot.register_next_step_handler(message, qiwi_check)



def qiwi_balance2(message):
    if message.text:
        if message.text == "Назад":
            bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
            bot.register_next_step_handler(message, main)
        else:
            text = message.text + ' ₽'
            qiwi = Image.open("Image source/qiwi_balance.png")
            fnt = ImageFont.truetype("Fonts/Roboto-Bold.ttf", 100)
            W = 1080
            w, h = fnt.getsize(text)
            d = ImageDraw.Draw(qiwi)
            d.text(((W-w)/2,296), text, font=fnt, fill=(255,255,255,255))
            del d
            qiwi.save("Image cache/file5.png", "PNG")
            img = open('Image cache/file5.png', 'rb')
            bot.send_photo(message.chat.id, img, reply_markup=back_keyboard_check())
            bot.register_next_step_handler(message, qiwi_balance3)
    else:
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBpp5fySJBsFYzrW_-3NIHuxhBXbKEZAACowoAAt-gOUkrfo6J91AWFx4E')
        bot.send_message(message.chat.id, "Ты еблан? Текст нужен")
        bot.register_next_step_handler(message, qiwi_balance2)

def qiwi_balance3(message):
    if message.text == "Вернуться в Меню🧭":
        bot.send_message(message.chat.id, "Возврат в меню...", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    elif message.text == "Ещё раз":
        bot.send_message(message.chat.id, "Какой баланс вы хотите?(Например 151,02. Знак ₽ поставится за вас!")
        bot.register_next_step_handler(message, qiwi_balance2)

if __name__ == '__main__':
    bot.polling(none_stop=True)