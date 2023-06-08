from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU, LEXICON_ADMIN
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
                callback_data='btn_admin_'+ button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data='btn_admin_'+ button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


btn_add: KeyboardButton = KeyboardButton(text=LEXICON_RU['btn_add'])
btn_menu: KeyboardButton = KeyboardButton(text=LEXICON_RU['menu_admin'])
admin_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[btn_add],[btn_menu]],
                                                    resize_keyboard=True)


admin_add_product_kb = create_inline_kb(2, 'cakes', 'cupcakes', 'bento_cake', 'Cake_to_go')

def admin_create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Добавляем в билдер ряд с кнопками
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON_ADMIN[button] if button in LEXICON_ADMIN else button,
        callback_data='admin_'+button) for button in buttons]).row(InlineKeyboardButton(text='УДАЛИТЬ', callback_data='удалить_admin')).row(InlineKeyboardButton(text='НАЗАД', callback_data='назад_admin'))
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


