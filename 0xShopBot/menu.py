from telebot import types
import telebot

select_conutry = types.InlineKeyboardMarkup(row_width=3)
select_conutry.add(
    types.InlineKeyboardButton(text='🇷🇺 Россия', callback_data='ru'),
    types.InlineKeyboardButton(text='🇺🇦 Украина', callback_data='ua'),
    types.InlineKeyboardButton(text='🇰🇿 Казахстан', callback_data='kz'),
    types.InlineKeyboardButton(text='🏳Моего города нету в списке', callback_data='selectsity')
)

select_city_ru = types.InlineKeyboardMarkup(row_width=3)
select_city_ru.add(
    types.InlineKeyboardButton(text='🇷🇺 Москва', callback_data='gomenu_check_check'),
    types.InlineKeyboardButton(text='🇷🇺 Санкт-Петербург', callback_data='gomenu_check_check'),
    types.InlineKeyboardButton(text='🇷🇺 Новосибирск', callback_data='gomenu_check_check'),
    types.InlineKeyboardButton(text='🇷🇺 Екантиренбург', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇷🇺 Нижний Новгород', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇷🇺 Казань', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇷🇺 Челябинск', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇷🇺 Омск', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇷🇺 Самара', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇷🇺 Ростов-на-Дону', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇷🇺 Уфа', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇷🇺 Красноярск', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇷🇺 Воронеж', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇷🇺 Перьм', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇷🇺 Волгоград', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇷🇺 Краснодар', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇷🇺 Саратов', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇷🇺 Тюмень', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇷🇺 Тольятти', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇷🇺 Ижевск', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇷🇺 Барнаул', callback_data='gomenu_check')
)
select_city_ua = types.InlineKeyboardMarkup(row_width=3)
select_city_ua.add(
    types.InlineKeyboardButton(text='🇺🇦 Киев', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇺🇦 Донецк', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇺🇦 Днепр', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇺🇦 Одесса', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇺🇦 Харьков', callback_data='gomenu_check')
)
select_city_kz = types.InlineKeyboardMarkup(row_width=3)
select_city_kz.add(
    types.InlineKeyboardButton(text='🇰🇿 Актобе', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇰🇿 Караганда', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇰🇿 Шмыкнет', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇰🇿 Астана', callback_data='gomenu_check'),
    types.InlineKeyboardButton(text='🇰🇿 Алматы', callback_data='gomenu_check'),
)


# Main menu
main_menu = types.InlineKeyboardMarkup(row_width=3)
main_menu.add(
    types.InlineKeyboardButton(text='🛍 Каталог', callback_data='catalog'),
    types.InlineKeyboardButton(text='👤 Профиль', callback_data='profile'),
    types.InlineKeyboardButton(text='ℹ Информация', callback_data='info'),
    types.InlineKeyboardButton(text='💸 Пополнить баланс', callback_data='replenish_balance'),
)
main_menu.add(
    types.InlineKeyboardButton(text='🎧 Обратиться в техподдержку', callback_data='support')
)


# Admin menu
admin_menu = types.InlineKeyboardMarkup(row_width=3)
admin_menu.add(types.InlineKeyboardButton(text='Управление каталогом', callback_data='catalog_control'))
admin_menu.add(types.InlineKeyboardButton(text='Управление товаром', callback_data='section_control'))
admin_menu.add(types.InlineKeyboardButton(text='Изменить баланс', callback_data='give_balance'))
admin_menu.add(types.InlineKeyboardButton(text='Рассылка', callback_data='admin_sending_messages'))
admin_menu.add(
    types.InlineKeyboardButton(text='Информация', callback_data='admin_info'),
    types.InlineKeyboardButton(text='Выйти', callback_data='exit_admin_menu')
)

# Admin control
admin_menu_control_catalog = types.InlineKeyboardMarkup(row_width=2)
admin_menu_control_catalog.add(
    types.InlineKeyboardButton(text='Добавить раздел в каталог', callback_data='add_section_to_catalog'),
    types.InlineKeyboardButton(text='Удалить раздел в каталог', callback_data='del_section_to_catalog'),
    types.InlineKeyboardButton(text='Назад', callback_data='back_to_admin_menu')
)

# Admin control section
admin_menu_control_section = types.InlineKeyboardMarkup(row_width=2)
admin_menu_control_section.add(
    types.InlineKeyboardButton(text='Добавить товар в раздел', callback_data='add_product_to_section'),
    types.InlineKeyboardButton(text='Удалить товар из раздела', callback_data='del_product_to_section'),
    types.InlineKeyboardButton(text='Назад', callback_data='back_to_admin_menu')
)

# Back to admin menu
back_to_admin_menu = types.InlineKeyboardMarkup(row_width=1)
back_to_admin_menu.add(
    types.InlineKeyboardButton(text='Вернуться в админ меню', callback_data='back_to_admin_menu')
)

btn_purchase = types.InlineKeyboardMarkup(row_width=2)
btn_purchase.add(
    types.InlineKeyboardButton(text='Купить', callback_data='buy'),
    types.InlineKeyboardButton(text='Выйти', callback_data='exit_to_menu')
)

btn_ok = types.InlineKeyboardMarkup(row_width=3)
btn_ok.add(
    types.InlineKeyboardButton(text='Понял', callback_data='btn_ok')
)

replenish_balance = types.InlineKeyboardMarkup(row_width=3)
replenish_balance.add(
    types.InlineKeyboardButton(text='🔄 Проверить', callback_data='check_payment'),
    types.InlineKeyboardButton(text='❌ Отменить', callback_data='cancel_payment')
)

to_close = types.InlineKeyboardMarkup(row_width=3)
to_close.add(
    types.InlineKeyboardButton(text='❌', callback_data='to_close')
)
