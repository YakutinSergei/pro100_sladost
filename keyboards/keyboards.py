from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU

# Функция для формирования инлайн-клавиатуры на лету
def create_inline_kb(width: int,
                     *args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON_RU[button] if button in LEXICON_RU else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


# ------- Создаем игровую клавиатуру без использования билдера -------

# Создаем кнопки игровой клавиатуры
btn_order: KeyboardButton = KeyboardButton(text=LEXICON_RU['order'])
order_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[btn_order]], resize_keyboard=True)

#Инлайн клавиатура выбора торта
order_select_kb = create_inline_kb(2, 'cakes','Cupcakes', 'bento_cake', 'Cake_to_go')