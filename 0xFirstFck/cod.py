 
from pyrogram import Client  # телеграм клиент
import shelve  # запись информации в файл
import random  # для выбора случайного элеменита из списка
import time  # для выбора случайного элеменита из списка
 
 
# Данные приложения телеграм (можно создать на my.telegram.org)
api_id = 183162
api_hash = "d89672a589c14e14129a713a01c86d0c"
phone_number = '+........'  # телефонный номер аккаунта в телеграме
PUBLIC = 'tupogram'  # паблик
# Варианты текстов сообщений
TEXTS = [
    'Круто !',
    'тоже так хочу 😎',
    '5 баллов 👍',
]
COMMENT_EVERY_N = 1  # комментируем каждое N собщение
                     # если равно 1, комментируем каждое сообщение
                     # если равно 3, комментируем каждое третье
                     # если равно 5, комментируем каждое пятое ... итд
 
# список обработанных сообщений
processed_messages = shelve.open('processed_messages.db',  # имя файла, куда писать
                                 writeback=True)
 
# создаем клиент телеграма
app = Client("python_cyberpunk", api_id, api_hash,
             phone_number=phone_number)
 
with app:
    public = app.get_chat(PUBLIC)  # ищем паблик по нику
    chat = public.linked_chat  # связанный чат обсуждений паблика
 
    while True:
        for msg in app.get_history(chat.id, limit=100):
            # фильтруем только авторепосты из паблика
            if (msg.from_user is None  # если сообщение не имеет автора
                    # и это репост из паблика (проверка по id)
                    and msg.forward_from_chat.id == public.id):
                if msg.forward_from_message_id % COMMENT_EVERY_N != 0:
                    print(f'Пропускаем message_id={msg.message_id},'
                        f' так как комментируе каждое {COMMENT_EVERY_N}')
                    continue
                # проверяем, есть ли в списке обработанных сообщений этот айди
                # чтобы не комментировать по несколько раз один пост
                if str(msg.forward_from_message_id) in processed_messages:
                    print(f'Пропускаем уже обработанное message_id={msg.message_id}')
                    continue
                # пишем в список обработанных айди этого сообщения
                processed_messages[str(msg.forward_from_message_id)] = True
 
                print(f'Обработка message_id={msg.message_id}')
 
                text = random.choice(TEXTS)  # выбираем случайный текст из списка
                app.send_message(chat.id, text,  # отправляем текст в чат
                                reply_to_message_id=msg.message_id)  # как ответ на сообщение с постом
 
                # для того, чтоб не оставлять больше одного коммента за 5 минут
                break  # выходим из перебора сообщений, если оставили коммент
 
        print('Ставим на паузу')
        time.sleep(60 * 5)
