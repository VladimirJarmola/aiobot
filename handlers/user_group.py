from string import punctuation

from aiogram import F, types, Router

from filters.chat_types import ChatTypesFilter


user_group_router = Router()
user_group_router.message.filter(ChatTypesFilter(['group', 'supergroup']))

restricted_words = {'кабан', 'хомяк', 'выхухоль'}

def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))


@user_group_router.edited_message() #отлавливаем запрещенные слова даже в отредактированных сообщениях
@user_group_router.message()
async def cleaner(message: types.Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f'{message.from_user.first_name}, собдюдайте порядок в чате!!!')
        await message.delete()
        # await message.chat.ban(message.from_user.id)
