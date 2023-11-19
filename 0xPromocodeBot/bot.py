import logging
import aiogram
from aiogram import Dispatcher, executor, types
import config, datetime, asyncio
from handlers import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from db.db import *

bot = aiogram.Bot(token=config.token)
dp = Dispatcher(bot, storage=MemoryStorage())

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger.error("Starting bot")


@dp.message_handler(text='Отмена', state='*')
async def cmd_test1(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Действие отменено.")


async def thread_stata():
    date_day = int(datetime.datetime.now().day)
    while True:
        if date_day != int(datetime.datetime.now().day):
            date_day = int(datetime.datetime.now().day)
            users = len(get_all_users())
            update_users(users)
        await asyncio.sleep(60)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(thread_stata())
    register_admins_handlers(dp)
    register_common_handlers(dp)
    executor.start_polling(dp, skip_updates=True)
