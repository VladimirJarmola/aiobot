from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.formatting import as_list, as_marked_section, Bold

from filters.chat_types import ChatTypesFilter
from kbds import reply


user_private_router = Router()
user_private_router.message.filter(ChatTypesFilter(['private', ]))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привет, я виртуальный помошник', 
                        reply_markup=reply.start_kb3.as_markup(
                            resize_keyboard=True,
                            input_field_placeholder="что Вас интересует",
                        ))


# @user_private_router.message(F.text.lower() == 'меню')
@user_private_router.message(or_f(Command('menu'), (F.text.lower() == 'меню')))
async def menu_cmd(message: types.Message):
    await message.answer('Вот меню: ', reply_markup=reply.del_kbd)


@user_private_router.message(F.text.lower() == 'о магазине')
@user_private_router.message(Command('about'))
async def about_cmd(message: types.Message):
    await message.answer('О нас: ', reply_markup=reply.test_kb)


@user_private_router.message(F.text.lower() == 'варианты оплаты')
@user_private_router.message(Command('payment'))
async def payment_cmd(message: types.Message):
    text = as_marked_section(
        Bold('Варианты оплаты: '),
        "Картой в боте",
        "При получении картой / кэш",
        "В заведении",
        marker='✅ ',
    )
    await message.answer(text.as_html())


@user_private_router.message((F.text.lower().contains('доставк')) | (F.text.lower() == 'варианты доставки'))
@user_private_router.message(Command('shipping'))
async def shipping_cmd(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold('Варианты доставки/заказа: '),
            "Курьер",
            "Самовынос",
            "у Вас",
            marker='✅ ',
        ),
        as_marked_section(
            Bold('Нельзя: '),
            "Почта",
            "Голуби",
            marker='❌',
        ),
        sep='\n-----------------\n'
    )
    await message.answer(text.as_html())


@user_private_router.message(F.contact)
async def get_contact(message: types.Message):
    await message.answer(f"Номер получен")
    await message.answer(str(message.contact.phone_number))


@user_private_router.message(F.location)
async def get_location(message: types.Message):
    await message.answer(f"локация получена")
    await message.answer(str(message.location))



# @user_private_router.message()
# async def echo(message: types.Message):
    # text = message.text

    # if text in ["Привет", "привет", "hi", "hello"]:
    #     await message.answer("И тебе привет!")
    # elif text in ["Пока", "пока", "пакеда", "До свидания"]:
    #     await message.answer("И тебе пока!")
    # else:
        # await message.answer(message.text)
    # await message.reply(message.text)
    # await message.answer(message.text)