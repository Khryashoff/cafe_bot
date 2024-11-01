from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keyboard(
        *btns: str,
        placeholder: str = None,
        request_contact: int = None,
        sizes: tuple[int] = (2,),
):
    navigation_keyboard = ReplyKeyboardBuilder()
    for index, text in enumerate(btns, start=0):
        if request_contact and request_contact == index:
            navigation_keyboard.add(
                KeyboardButton(text=text, request_contact=True)
            )

        else:
            navigation_keyboard.add(KeyboardButton(text=text))

    return navigation_keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True,
        input_field_placeholder=placeholder
    )
