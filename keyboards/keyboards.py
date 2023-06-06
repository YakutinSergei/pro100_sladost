from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_RU, LEXICON, calendar


#КАЛЕНДАРИ
def create_inline_date_kb(
                     btn_1: str,
                     btn_2: str,
                     btn_3) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    btn_2 = calendar[btn_2][0]


    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(InlineKeyboardButton(text=btn_1, callback_data='days_btn'), InlineKeyboardButton(text=btn_2, callback_data='month_btn'),
                                        InlineKeyboardButton(text=btn_3, callback_data='year_btn')).row(InlineKeyboardButton(text='ОК', callback_data='ok'))

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

def create_inline_day_kb(month, year) ->InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    if calendar[month] == 'февраль':
        if int(year) % 4 != 0:
            month = 28
        elif int(year) % 100 == 0:
            if int(year) % 400 == 0:
                month = 29
            else:
                month = 28
        else:
            month = 29
    else:
        month = int(calendar[month][1])

    buttons: list[InlineKeyboardButton] = []

    for i in range(1,month+1):
        buttons.append(InlineKeyboardButton(
            text=str(i),
            callback_data='day_'+str(i)))

        # Распаковываем список с кнопками в билдер методом row c параметром width

    kb_builder.row(*buttons, width=7)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

def create_inline_month_kb() ->InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    buttons: list[InlineKeyboardButton] = []

    for i in range(1, 13):
        buttons.append(InlineKeyboardButton(
            text=calendar[str(i)][0],
            callback_data='mounth_' + str(i)))

        # Распаковываем список с кнопками в билдер методом row c параметром width

    kb_builder.row(*buttons, width=3)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

def create_inline_year_kb(year) ->InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    buttons: list[InlineKeyboardButton] = []

    for i in range(int(year), int(year)+2):
        buttons.append(InlineKeyboardButton(
            text=str(i),
            callback_data='year_' + str(i)))

        # Распаковываем список с кнопками в билдер методом row c параметром width

    kb_builder.row(*buttons, width=2)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

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


#пагинация
def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Добавляем в билдер ряд с кнопками
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON[button] if button in LEXICON else button,
        callback_data=button) for button in buttons]).row(InlineKeyboardButton(text=LEXICON_RU['order'], callback_data=LEXICON_RU['order'])).row(InlineKeyboardButton(text='НАЗАД', callback_data='назад'))
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# ------- Создаем игровую клавиатуру без использования билдера -------

# Создаем кнопки игровой клавиатуры
btn_menu: KeyboardButton = KeyboardButton(text=LEXICON_RU['menu'])
order_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[btn_menu]], resize_keyboard=True)

#Инлайн клавиатура выбора торта
order_select_kb = create_inline_kb(2, 'cakes','cupcakes', 'bento_cake', 'Cake_to_go')