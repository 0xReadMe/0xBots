#бот пересылает сообщения админу
import telebot, time
admin = False # enter your id
callback = False
bot = telebot.TeleBot(input())

def reply_keyboard(user_id):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text='reply', callback_data=str(user_id)))
    return keyboard


def start_bot():
    @bot.message_handler(commands=['start'])
    def start_message(message):
        global admin, callback
        if not admin:
            admin = message.chat.id
            bot.send_message(admin, f'Приветствую, admin')     


    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        global admin, callback
        if message.chat.id != admin:
            bot.send_message(admin, f'new message\nfrom: id{message.chat.id}, @{message.from_user.username}\n{message.text}', reply_markup = reply_keyboard(message.chat.id))
        else: 
            if callback:
                bot.reply_to(message, f'the message was successfully delivered | recipient id{callback}')
                bot.send_message(int(callback), f'response from admin:\n{message.text}')
            callback = False
                
            
            
    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call): 
        global admin, callback
        bot.answer_callback_query(callback_query_id=call.id, text='enter a message')
        callback = call.data
        
        
    while True:
        try:
            print('Бот в процессе запуска...')
            bot.polling(none_stop=True)
        except Exception as e:
            print(f'Критическая ошибка:\n{e}\n')
            print('Бот был выключен на 2 минуты, пожалуйста, ждите')
            time.sleep(120)

start_bot()
