from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram import Router, F
from aiogram.filters import Command, Text
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.fsm.storage.memory import MemoryStorage
from create_bot import bot
from data_base.postreSQL_bd import postres_add_command, postreSQL_read, postreSQL_user_read, postreSQL_pg_up, \
    postreSQL_up, postreSQL_del
from keyboards.admin_kb import admin_kb, admin_add_product_kb, admin_create_pagination_keyboard

admin_list = [654222332]
pg = 0
len_pg = 0
res = dict()



storage: MemoryStorage = MemoryStorage()

ID = None

product = []

router: Router = Router()

class FSMAdmin(StatesGroup):
    category = State()
    photos = State()
    name = State()
    discription = State()
    price = State()

#Начало добавление
@router.message(Text(text=LEXICON_RU['btn_add']), StateFilter(default_state))
async def process_add_photo_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['selecting_cat'], reply_markup=admin_add_product_kb)
    await state.set_state(FSMAdmin.category)

@router.message(Text(text='Отмена'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Вы и не начинали добавлять')


@router.message(Text(text='Отмена'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Добавление отменено')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()

@router.callback_query(StateFilter(FSMAdmin.category))
async def add_cake_bd(calllback: CallbackQuery, state: FSMContext):
    await state.update_data(category=calllback.data)
    await calllback.message.answer(text=LEXICON_RU['add_photo'])
    await state.set_state(FSMAdmin.photos)

#Загрузка названия
@router.message(StateFilter(FSMAdmin.photos), F.photo[-1].as_('largest_photo'))
async def process_add_name_command(message: Message, state: FSMContext):

    # Cохраняем введенное имя в хранилище по ключу "photo"
    await state.update_data(photos=message.photo[0].file_id)

    await message.reply(text='Введите название:')
    await state.set_state(FSMAdmin.name)

@router.message(StateFilter(FSMAdmin.photos))
async def warning_not_photo(message: Message):
    await message.answer(text='Пожалуйста, на этом шаге отправьте '
                              'фото товара\n\nЕсли вы хотите прервать '
                              'заполнение карточки товара - отправьте команду /cancel')


#Загрузка описания
@router.message(StateFilter(FSMAdmin.name))
async def process_add_desc_command(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.reply(text='Введите описание')
    await state.set_state(FSMAdmin.discription)



#Загрузка цены
@router.message(StateFilter(FSMAdmin.discription))
async def process_add_price_command(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.reply(text='Введите цену')
    await state.set_state(FSMAdmin.price)

# Завершаюший машина состояние
@router.message(StateFilter(FSMAdmin.price), lambda x: x.text.isdigit())
async def process_add_bd(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    product = await state.get_data()
    await state.clear()
    postres_add_command(product)
    await message.answer(text=LEXICON_RU['add_entry'])

# Этот хэндлер будет срабатывать, если во время ввода Цены
# будет введено что-то некорректное
@router.message(StateFilter(FSMAdmin.price))
async def warning_not_age(message: Message):
    await message.answer(
        text='Цена должна содержать только цифры\n\n'
             'Попробуйте еще раз\n\nЕсли вы хотите прервать '
             'заполнение карточки продукта - отправьте команду /cancel')


#Проверка на хозяина
@router.message(Command(commands=['admin']))
async def process_moderator_command(message: Message):
    user_up = postreSQL_user_read(message.from_user.id)
    if user_up[0][-1] == 'admin':
        await bot.send_message(message.from_user.id, text='Что надо хозяин', reply_markup=admin_kb)
    else:
        await bot.send_message(message.from_user.id, text='Вы не являетесь администратором')


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний

@router.message(Text(text=LEXICON_RU['menu_admin']))
async def procces_menu_command(message: Message):
    await message.answer(text='Выбирите категорию', reply_markup=admin_add_product_kb)


@router.callback_query(Text(text='admin_forward'))
async def process_forward_press(callback: CallbackQuery):
    user_up = postreSQL_user_read(callback.from_user.id)
    res = postreSQL_read(user_up[0][2])
    len_pg = len(res)
    if int(user_up[0][3]) + 1 < len_pg:
        pg = postreSQL_pg_up(callback.from_user.id, 1)
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(media=res[pg][2],
                                  caption=f'{res[pg][3]}\nОписание: {res[pg][4]}\n Цена:{res[pg][-1]}'),
            reply_markup=admin_create_pagination_keyboard('backward',
                                                    f'{pg + 1}/{len_pg}',
                                                    'forward'))

    await callback.answer()

@router.callback_query(Text(text='admin_backward'))
async def process_forward_press(callback: CallbackQuery):
    user_up = postreSQL_user_read(callback.from_user.id)
    res = postreSQL_read(user_up[0][2])
    len_pg = len(res)
    if int(user_up[0][3]) > 0:
        pg = postreSQL_pg_up(callback.from_user.id, -1)
        if pg < len_pg:
            await bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=InputMediaPhoto(media=res[pg][2],
                                      caption=f'{res[pg][3]}\nОписание: {res[pg][4]}\n Цена:{res[pg][-1]}'),
                reply_markup=admin_create_pagination_keyboard('backward',
                                                              f'{pg + 1}/{len_pg}',
                                                              'forward'))

    await callback.answer()


#Кнопка назад
@router.callback_query(Text(text='назад_admin'))
async def back_category_command(callback: CallbackQuery):
    await callback.message.answer(text='Выбирите категорию', reply_markup=admin_add_product_kb)
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.answer()

@router.callback_query(Text(text='удалить_admin'))
async def del_product_command(callback: CallbackQuery):
    user_up = postreSQL_user_read(callback.from_user.id)
    res = postreSQL_read(user_up[0][2])
    postreSQL_del(res[int(user_up[0][3])][3])
    res.pop(int(user_up[0][3]))
    if len(res) == 0:
        await callback.message.answer(text='Выбирите категорию', reply_markup=admin_add_product_kb)
    else:
        len_pg = len(res)
        if int(user_up[0][3]) >= len_pg:
            pg = postreSQL_pg_up(callback.from_user.id, -1)
        await bot.send_photo(chat_id=callback.from_user.id, photo=res[pg][2],
                             caption=f'{res[pg][3]}\nОписание: {res[pg][4]}\n Цена:{res[pg][-1]}',
                             reply_markup=admin_create_pagination_keyboard('backward',
                                                                           f'{pg + 1}/{len_pg}',
                                                                           'forward'))
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.answer()


#Отображение клавиатуры
@router.callback_query(Text(startswith='btn_'))
async def print_categoryes_cammand(callback: CallbackQuery):
    res = postreSQL_read(callback.data)
    pg = 0
    users_up = postreSQL_up(callback.from_user.id, pg, callback.data)
    len_pg = len(res)
    if len_pg > 0:
        await bot.send_photo(chat_id=callback.from_user.id, photo=res[pg][2],
                             caption=f'{res[pg][3]}\nОписание: {res[pg][4]}\n Цена:{res[pg][-1]}',
                             reply_markup=admin_create_pagination_keyboard('backward',
                                                                     f'{pg + 1}/{len_pg}',
                                                                     'forward'))
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.answer()