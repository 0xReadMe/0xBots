from aiogram import Dispatcher
from keyboards import *
from db.db import *
from aiogram.dispatcher import FSMContext


async def message_hello(message: types.Message):
    new_user(message.from_user.id)
    await message.bot.send_photo(chat_id=message.chat.id, caption=get_hello_text(),
                                 photo='AgACAgIAAxkBAAMmYSjE94gh4be_xmkvwTx2ePAmzvgAAsS0MRtn9UlJcDqAx6-HZJABAAMCAANzAAMgBA',
                                 reply_markup=keyboard_users, parse_mode=types.ParseMode.HTML)
async def message_menu(message: types.Message):
    await message.bot.send_photo(chat_id=message.chat.id,caption="Меню бота:\n1) Получить промокоды\n2) Связь с администрацией",
                                 photo='AgACAgIAAxkBAAMmYSjE94gh4be_xmkvwTx2ePAmzvgAAsS0MRtn9UlJcDqAx6-HZJABAAMCAANzAAMgBA', reply_markup=keyboard_users, parse_mode=types.ParseMode.HTML)

async def message_promo(message: types.Message):
    await message.answer(get_promo_text(), reply_markup=keyboard_users, parse_mode=types.ParseMode.HTML)


async def message_admin(message: types.Message):
    await message.answer(get_admin_text(), reply_markup=keyboard_users, parse_mode=types.ParseMode.HTML)


def register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(message_promo, lambda message: is_user(int(message.from_user.id)), text='Получить промокоды')
    dp.register_message_handler(message_admin, lambda message: is_user(int(message.from_user.id)), text='Связь с администрацией')
    dp.register_message_handler(message_menu, lambda message: is_user(int(message.from_user.id)))
    dp.register_message_handler(message_hello, lambda message: not is_user(int(message.from_user.id)))


