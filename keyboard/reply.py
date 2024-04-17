from aiogram.types import KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder


navigation_keyboard = ReplyKeyboardBuilder()

navigation_keyboard.add(
    KeyboardButton(text='Меню'),
    KeyboardButton(text='О нас'),
    KeyboardButton(text='Заказать доставку'),
    KeyboardButton(text='Варианты оплаты'),
)
navigation_keyboard.adjust(2, 2)

hide_navigation_keyboard = ReplyKeyboardRemove()
