# -*- coding: utf-8 -*-

from traceback import format_exc

import config
from main import Bot

try:
    Bot(
        phone=config.number,
        qiwiApi=config.tokenQiwi,
        token=config.token,
        admins=config.admins,
    )

except:
    print(f"Произошла ошибка: {format_exc()}")
    input("Нажми Enter ")
