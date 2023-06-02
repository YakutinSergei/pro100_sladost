from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters import Command, CommandStart, Text
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.fsm.storage.memory import MemoryStorage
from create_bot import bot
from data_base.sqlite_bd import sql_add_command
from keyboards.admin_kb import admin_kb



storage: MemoryStorage = MemoryStorage()

ID = None


router: Router = Router()

class FSMAdmin(StatesGroup):
    photos = State()
    name = State()
    discription = State()
    price = State()

#Начало диалога
@router.message(Text(text=LEXICON_RU['btn_add']), StateFilter(default_state))
async def process_add_photo_command(message: Message, state: FSMContext):
    if message.from_user.id == ID:
        await message.reply(text=LEXICON_RU['add_photo'])
        await state.set_state(FSMAdmin.photos)


#Загрузка названия
@router.message(StateFilter(FSMAdmin.photos))
async def process_add_name_command(message: Message, state: FSMContext):
    if message.from_user.id == ID:
        # Cохраняем введенное имя в хранилище по ключу "photo"
        await state.update_data(photos=message.photo[0].file_id)

        await message.reply(text='Введите название:')
        await state.set_state(FSMAdmin.name)


#Загрузка описания
@router.message(StateFilter(FSMAdmin.name))
async def process_add_desc_command(message: Message, state: FSMContext):
    if message.from_user.id == ID:
        await state.update_data(name=message.text)

        await message.reply(text='Введите описание')
        await state.set_state(FSMAdmin.discription)



#Загрузка цены
@router.message(StateFilter(FSMAdmin.discription))
async def process_add_price_command(message: Message, state: FSMContext):
    if message.from_user.id == ID:
        await state.update_data(description=message.text)
        await message.reply(text='Введите цену')
        await state.set_state(FSMAdmin.price)

# Завершаюший машина состояние
@router.message(StateFilter(FSMAdmin.price))
async def process_add_bd(message: Message, state: FSMContext):
    await state.update_data(price=float(message.text))
    await sql_add_command(state)
    await state.clear()
    await message.answer(text=LEXICON_RU['add_entry'])






#Проверка на хозяина
@router.message(Command(commands=['moderator']))
async def process_moderator_command(message: Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, text='Что надо хозяин', reply_markup=admin_kb)

# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@router.message(Command(commands=['cancel']), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего. Вы вне машины состояний\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /fillform')


@router.message(Command(commands=['cancel']), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Вы вышли из машины состояний\n\n'
                              'Чтобы снова перейти к заполнению анкеты - '
                              'отправьте команду /fillform')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()