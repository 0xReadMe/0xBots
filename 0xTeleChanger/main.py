from telethon import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.account import UpdateProfileRequest
import os
import time
import random

api_id = 0000 # заменить на свое
api_hash = 'apihash' # заменить на свое
picture_path = 'путь\\до\\папки\\изображений'
# заменить в случае использования Linux
#picture_path = '/путь/до/Изображения/'

client = TelegramClient('имя', api_id, api_hash)


async def main():
    while True:
        files = os.listdir(picture_path)
        rnd_files = random.sample(files, len(files))
        print('Перемешиваем фотки..')
        for picture in rnd_files:
            rnd = random.randint(1, 489)
            print(f'Фото сменится через {rnd} секунд')
            await client(DeletePhotosRequest(
                await client.get_profile_photos('me')))
            await client(UploadProfilePhotoRequest(
                await client.upload_file(picture_path + '\\' + picture)))
                # заменить в случае использования Linux
                #await client.upload_file(picture_path + picture)))
            with open('usernames.txt', encoding="utf8") as usernames:
                text = usernames.read().splitlines()
                rnd_username = random.sample(text, len(text))
                print('Перемешиваем имена...')
                rnd_choice = random.randint(0, len(rnd_username)-1)
                username = rnd_username[rnd_choice]
                print(f'Выбрали имя {username}')
                await client(UpdateProfileRequest(first_name=f'{username}'))
            time.sleep(rnd)


with client:
    client.loop.run_until_complete(main())
