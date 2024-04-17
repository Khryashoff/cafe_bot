from aiogram import Router, F, types
from aiogram.filters import Command, CommandStart, or_f
from aiogram.utils.formatting import as_marked_section

from keyboard.reply import navigation_keyboard


user_router = Router()


@user_router.message(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(
        text='Благодарю за обращение!',
        reply_markup=navigation_keyboard.as_markup(
            resize_keyboard=True,
            input_field_placeholder='Что Вас интересует?'
        )
    )


@user_router.message(or_f(Command('menu'), (F.text.lower() == 'меню')))
async def bot_menu(message: types.Message):
    await message.answer('Меню пока нет, но скоро будет, окей?')


@user_router.message(Command('about_us'))
async def bot_about_us(message: types.Message):
    await message.answer('Извини, но пока мне нечего рассказать.')


@user_router.message(
    or_f(Command('payment'), (F.text.lower().contains('оплат')))
)
async def bot_payment(message: types.Message):
    text = as_marked_section(
        'Варианты оплаты:',
        'Картой через бота',
        'При получении картой',
        'При получении наличными (без сдачи)',
        'При получении наличными (нужна сдача)',
        'В заведении наличными или картой',
        marker='✅ '
    )
    await message.answer(text.as_html())


@user_router.message(
    or_f(Command('delivery'), (F.text.lower().contains('доставк')))
)
async def bot_delivery(message: types.Message):
    text = as_marked_section(
        'Доставка курьером на адрес:',
        'Платная доставка по городу 150 рублей',
        'Бесплатная доставка по городу при заказе от 550 рублей',
        marker='✅ '
    )
    await message.answer(text.as_html())
