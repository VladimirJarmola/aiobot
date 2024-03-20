import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv()) #подключаем переменные окружения

from handlers.user_private import user_private_router
from handlers.user_group import user_group_router
from common.bot_cmds_list import private

ALLOWED_UPDATES = ['message, edited_message']

bot = Bot(
    token=os.getenv('TOKEN'), 
    default=DefaultBotProperties(parse_mode=ParseMode.HTML) # включаем html разметку для всего проекта
)
dp = Dispatcher()

#подключаем хендлеры
dp.include_router(user_private_router)
dp.include_router(user_group_router)#хэндлер групп ниже личных, иначе он будет отлавливать все сообщения и до приватных не дойдет

async def main():
    await bot.delete_webhook(drop_pending_updates=True) #очищает очередь необоработанных сообщений
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats()) #Прогрмано удаляется меню бота
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats()) #програмно задается меню бота
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())