from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters.chat_access_level import IsAdmin
from keyboard.reply import get_keyboard


admin_router = Router()
admin_router.message.filter(IsAdmin())


ADMIN_KEYBOARD = get_keyboard(
    'Добавить товар',
    'Изменить товар',
    'Удалить товар',
    'Просмотреть существующие товары',
    placeholder='Выберите действие',
    sizes=(2, 1, 1),
)


@admin_router.message(Command('admin'))
async def admin_start(message: types.Message):
    await message.answer('Что нужно сделать?', reply_markup=ADMIN_KEYBOARD)


@admin_router.message(F.text == 'Изменить товар')
async def change_product(message: types.Message):
    await message.answer('Вот список добавленных товаров:')


@admin_router.message(F.text == 'Удалить товар')
async def delete_product(message: types.Message):
    await message.answer('Выберите, что нужно удалить:')


@admin_router.message(F.text == 'Просмотреть существующие товары')
async def view_product(message: types.Message):
    await message.answer('Вот список добавленных товаров:')


class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    texts = {
        'AddProduct:name': 'Введите название товара:',
        'AddProduct:description': 'Введите описание товара',
        'AddProduct:price': 'Введите стоимость товара',
        'AddProduct:image': 'Добавьте новое изображение товара'
    }


@admin_router.message(StateFilter(None), F.text == 'Добавить товар')
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        'Введите название товара', reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)


@admin_router.message(StateFilter('*'), Command('Отмена'))
@admin_router.message(StateFilter('*'), F.text.casefold() == 'Отмена')
async def cancel_action(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(text='Действие отменено', reply_markup=ADMIN_KEYBOARD)


@admin_router.message(StateFilter('*'), Command('Назад'))
@admin_router.message(StateFilter('*'), F.text.casefold() == 'Назад')
async def step_back_action(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == AddProduct.name:
        await message.answer(
            'Вы находитесь на первом шаге, введите название товара или '
            'напишите "Отмена"'
        )
        return

    previous_step = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous_step)
            await message.answer(
                f'Вы вернулись к предыдущему шагу '
                f'{AddProduct.texts[previous_step.state]}'
            )
            return
        previous_step = step


@admin_router.message(AddProduct.name, F.text)
async def add_name_product(message: types.Message, state: FSMContext):
    if len(message.text) >= 100:
        await message.answer(
            'ОШИБКА: Название товара не должно превышать 100 символов, '
            'пожалуйста введите название заново!'
        )
        return

    await state.update_data(name=message.text)
    await message.answer('Введите описание товара')
    await state.set_state(AddProduct.description)


@admin_router.message(AddProduct.name)
async def wrong_name_product(message: types.Message, state: FSMContext):
    await message.answer(
        'ОШИБКА: Вы ввели недопустимые данные, '
        'пожалуйста введите название заново!'
    )


@admin_router.message(AddProduct.description, F.text)
async def add_description_product(message: types.Message, state: FSMContext):
    if len(message.text) >= 1000:
        await message.answer(
            'ОШИБКА: Описание товара не должно превышать 1000 символов, '
            'пожалуйста введите описание заново!'
        )
        return

    await state.update_data(description=message.text)
    await message.answer('Введите стоимость товара')
    await state.set_state(AddProduct.price)


@admin_router.message(AddProduct.description)
async def wrong_description_product(message: types.Message, state: FSMContext):
    await message.answer(
        'ОШИБКА: Вы ввели недопустимые данные, '
        'пожалуйста введите описание снова'
    )


@admin_router.message(AddProduct.price, F.text)
async def add_price_product(message: types.Message, state: FSMContext):
    try:
        float(message.text)
    except ValueError:
        await message.answer('ОШИБКА: Введите корректное значение стоимости!')
        return

    await state.update_data(price=message.text)
    await message.answer('Выберите изображение для карточки товара')
    await state.set_state(AddProduct.image)


@admin_router.message(AddProduct.price)
async def wrong_price_product(message: types.Message, state: FSMContext):
    await message.answer(
        'ОШИБКА: Вы ввели недопустимые данные, '
        'пожалуйста введите стоимость заново!'
    )


@admin_router.message(AddProduct.image, F.photo)
async def add_image_product(message: types.Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer(
        'Карточка товара успешно добавлена', reply_markup=ADMIN_KEYBOARD
    )
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()


@admin_router.message(AddProduct.image)
async def wrong_image_product(message: types.Message, state: FSMContext):
    await message.answer(
        'ОШИБКА: Вы отправляете недопустимые данные, '
        'пожалуйста загрузите фотографию заново!'
    )
