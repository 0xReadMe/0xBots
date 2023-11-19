from aiogram import types
keyboard_users = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
keyboard_users.add('Связь с администрацией', 'Получить промокоды')


keyboard_admin = types.InlineKeyboardMarkup()
keyboard_admin.add(types.InlineKeyboardButton(text='Рассылка', callback_data=f"spam"))
keyboard_admin.add(types.InlineKeyboardButton(text='Статистика', callback_data=f"stata"))
keyboard_admin.add(types.InlineKeyboardButton(text='Изменить текста', callback_data=f"edittext"))
keyboard_admin.add(types.InlineKeyboardButton(text='Получить текст', callback_data=f"gettext"))


keyboard_edit_text = types.InlineKeyboardMarkup()
keyboard_edit_text.add(types.InlineKeyboardButton(text='Приветсвие', callback_data=f"edithello"))
keyboard_edit_text.add(types.InlineKeyboardButton(text='Связь с администрацией', callback_data=f"editadmin"))
keyboard_edit_text.add(types.InlineKeyboardButton(text='Получить промокоды', callback_data=f"edithpromo"))
keyboard_edit_text.add(types.InlineKeyboardButton(text='Отмена', callback_data=f"close"))

keyboard_close = types.InlineKeyboardMarkup()
keyboard_close.add(types.InlineKeyboardButton(text='Отмена', callback_data=f"close"))


keyboard_confirmation = types.InlineKeyboardMarkup()
keyboard_confirmation.add(types.InlineKeyboardButton(text='ПОДТВЕРЖДАЮ', callback_data=f"yes"))
keyboard_confirmation.add(types.InlineKeyboardButton(text='Отмена', callback_data=f"close"))