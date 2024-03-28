import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv()) #подключаем переменные окружения

from common.bot_cmds_list import private

from database.engine import create_db, drop_db, session_maker

from handlers.user_private import user_private_router
from handlers.admin_private import admin_router
from handlers.user_group import user_group_router

from middlewares.db import DataBaseSession

# ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query']
# используемые апдейты автоматически буду использоваться, если передать в старт полинг allowed_updates=dp.resolve_used_update_types()

bot = Bot(
    token=os.getenv('TOKEN'), 
    default=DefaultBotProperties(parse_mode=ParseMode.HTML) # включаем html разметку для всего проекта
)
bot.my_admins_list=[]

dp = Dispatcher()

#подключаем миддлвар
# admin_router.message.middleware(CounterMiddleware())
# dp.update.outer_middleware(CounterMiddleware())

#подключаем хендлеры
dp.include_router(user_private_router)
dp.include_router(user_group_router)#хэндлер групп ниже личных, иначе он будет отлавливать все сообщения и до приватных не дойдет
dp.include_router(admin_router)

async def on_startup(bot):
    run_param = False #дополнительный параметр для очистки дб, можно реализовать передачу через кмд при запуске
    if run_param:
        await drop_db()
    await create_db()

async def on_shutdown(bot):
    print('Бот лег')


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True) #очищает очередь необоработанных сообщений
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats()) #Прогрмано удаляется меню бота
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats()) #програмно задается меню бота
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())
