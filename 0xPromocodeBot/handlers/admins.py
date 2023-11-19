from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import *
import asyncio

from db.db import *


async def send_spam(text, bot):
    i = 0
    for user in set(get_all_users()):
        user_id = user[0]
        if i > 15:
            await asyncio.sleep(1)
            i = 0
        i += 1
        try:
            await bot.send_message(chat_id=user_id, text=text, parse_mode=types.ParseMode.HTML)
        except Exception as e:
            print(e)
            if str(e) == 'Forbidden: bot was blocked by the user':
                del_user(user_id)
                print(user_id, 'меня заблокировал')


async def message_admin(message: types.Message):
    admins = list(get_admins())
    for i in range(len(admins)):
        admins[i] = f'<a href="tg://user?id={admins[i][0]}">{admins[i][0]}</a>'
    text = 'Админы:\n' + '\n'.join(admins) + '\nДобавить админа /newadm |id|\nУбрать админа /deladm |id|\n\nПример:\n/newadm 14881337228'
    await message.answer(text + '\n\nАдмин панелька:', reply_markup=keyboard_admin, parse_mode=types.ParseMode.HTML)


async def message_close_message(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text('Действие отменено', reply_markup=keyboard_admin)



async def message_stata(call: types.CallbackQuery):
    all_users = len(get_all_users())
    users = get_users()
    await call.message.edit_text(f'СТАТИСТИКА:\nЗа сегодня {all_users - users} юзеров\nВсего: {all_users} юзеров', reply_markup=keyboard_admin)



# изменение текстов
class OrderEdit(StatesGroup):
    what = State()
    text = State()
    confirmation = State()


async def message_edit(call: types.CallbackQuery):
    await call.message.edit_text('выбери:', reply_markup=keyboard_edit_text)
    await OrderEdit.what.set()


async def message_edit_what(call: types.CallbackQuery, state: FSMContext):
    what = call.data
    await state.update_data(what=what)
    await OrderEdit.text.set()
    await call.message.edit_text('введи текст', reply_markup=keyboard_close)


async def message_edit_text(message: types.Message, state: FSMContext):
    text = message.html_text
    await state.update_data(text=text)
    await OrderEdit.confirmation.set()
    await message.answer('Да?', reply_markup=keyboard_confirmation)


async def message_edit_confirmation(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    if data['what'] == 'edithello':
        edit_text_hello(data['text'])
    elif data['what'] == 'editadmin':
        edit_text_admin(data['text'])
    else:
        edit_text_promo(data['text'])
    await call.message.edit_text('успешно', reply_markup=keyboard_admin)


# вывод текста в html5
class OrderGettext(StatesGroup):
    text = State()

async def message_get_text(call: types.CallbackQuery):
    await OrderGettext.text.set()
    await call.message.edit_text(f"введите текст", reply_markup=keyboard_close)


async def message_get_text2(message: types.Message, state: FSMContext):
    await state.finish()
    text = message.html_text
    await message.answer(text, reply_markup=keyboard_admin)


# рассылка
class OrderSpam(StatesGroup):
    text = State()
    confirmation = State()



async def message_spam(call: types.CallbackQuery):
    await OrderSpam.text.set()
    await call.message.edit_text(f"введите текст", reply_markup=keyboard_close)


async def message_spam_text(message: types.Message, state: FSMContext):
    text = message.html_text
    await state.update_data(text=text)
    await OrderSpam.confirmation.set()
    await message.answer('Да?', reply_markup=keyboard_confirmation)


async def message_spam_confirmation(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    await send_spam(data['text'], call.message.bot)
    await call.message.edit_text('успешно', reply_markup=keyboard_admin)


async def message_new_admin(message: types.Message):
    new_admin(message.text.split()[-1])
    await message.answer('good!')


async def message_del_admin(message: types.Message):
    del_admin(message.text.split()[-1])
    await message.answer('good!')


def register_admins_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(message_close_message, text='close', state='*')
    dp.register_callback_query_handler(message_edit, text='edittext')
    dp.register_callback_query_handler(message_edit_what, state=OrderEdit.what)
    dp.register_message_handler(message_edit_text, state=OrderEdit.text)
    dp.register_callback_query_handler(message_edit_confirmation, state=OrderEdit.confirmation, text='yes')

    dp.register_callback_query_handler(message_spam, text='spam')
    dp.register_message_handler(message_spam_text, state=OrderSpam.text)
    dp.register_callback_query_handler(message_spam_confirmation, state=OrderSpam.confirmation, text='yes')

    dp.register_callback_query_handler(message_get_text, text='gettext')
    dp.register_message_handler(message_get_text2, state=OrderGettext.text)

    dp.register_callback_query_handler(message_stata, text='stata')

    dp.register_message_handler(message_new_admin, lambda message: (is_admin(message.from_user.id) or len(get_admins()) == 0) and '/newadm ' in message.text)
    dp.register_message_handler(message_new_admin, lambda message: is_admin(message.from_user.id) and '/deladm ' in message.text)



    dp.register_message_handler(message_admin, lambda message: is_admin(message.from_user.id), text='/admin')
