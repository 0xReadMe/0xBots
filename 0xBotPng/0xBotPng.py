from PIL import Image
import requests
import os

import telebot
bot = telebot.TeleBot('токен')
 

@bot.message_handler(content_types=['photo'])
def photo(message):
    raw = message.photo[-1].file_id
    name = str(message.chat.id) + '.jpg'
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(name,'wb') as new_file:
        new_file.write(downloaded_file)
    
    img = Image.open(name)
    x, y = img.size
    if not img.mode == 'RGB':
        img = img.convert('RGB')
    p_img = img.load()
    for i in range(x):
        for j in range(y):
            p_img[i, j] = (
                int(list(map(lambda p: p, [p_img[i, j][0]]))[0]),
                int(list(map(lambda p: 0, [p_img[i, j][1]]))[0]),
                int(list(map(lambda p: 0, [p_img[i, j][2]]))[0])
            )
    image = img        
    image.save(name)
    with open(name, "rb") as file:
        data = file.read()
    bot.send_photo(message.from_user.id, photo=data)

    os.remove(name)
    
    
     
bot.polling()
