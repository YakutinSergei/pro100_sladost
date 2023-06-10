import asyncio

from aiogram import Router, F
from datetime import datetime
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.filters import Command, Text
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from create_bot import bot
from data_base.postreSQL_bd import postreSQL_user_read, postreSQL_read
from keyboards.keyboards import create_inline_month_kb, create_inline_year_kb, create_inline_date_kb, create_inline_day_kb, create_inline_kb
from lexicon.lexicon_ru import LEXICON_RU

router: Router = Router()


# переделать в машинное состояние
mediagroups = {}
day = str(datetime.now().day)
mouth = str(datetime.now().month)
year = str(datetime.now().year)
order_product = []
new_album = [] #Альбом фотографий

#Машиносостояние
class FSMorder(StatesGroup):
    category = State()
    name_user = State() #Ваше имя
    telephon = State() #Номер для связи
    data_order = State() #Дата заказа
    quantity = State() #Количество
    filling = State() #Начинка
    decor = State() #Декор
    delivery = State() #способ доставки



@router.callback_query(Text(text=LEXICON_RU['order']), StateFilter(default_state))
async def order_add_command(callback: CallbackQuery, state: FSMContext):
    user_up = postreSQL_user_read(callback.from_user.id)
    res = postreSQL_read(user_up[0][2])
    await state.update_data(category=str(res[int(user_up[0][3])][1]).split('_')[-1])
    await callback.message.answer(text='Как к Вам можно обращаться: ')
    await callback.answer()
    await state.set_state(FSMorder.name_user)

@router.message(StateFilter(FSMorder.name_user))
async def order_telephon_command(message: Message, state: FSMContext):
    await state.update_data(name_user=message.text)

    await message.answer(text='Укажите номер телефона для связи')
    await state.set_state(FSMorder.telephon)

@router.message(StateFilter(FSMorder.telephon))
async def order_date_process(message: Message, state: FSMContext):
    global day, mouth, year
    await state.update_data(telephon=message.text)
    await message.answer(text='Выберите дату заказа', reply_markup=create_inline_date_kb(day, mouth, year))


#Клавиатура выбора дня
@router.callback_query(Text(text='days_btn'))
async def calendar_days_process(callback: CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                         reply_markup=create_inline_day_kb(str(datetime.now().month), str(datetime.now().year)))


#Выбераем день
@router.callback_query(Text(startswith='day_'))
async def calendar_choice_day_procces(callback: CallbackQuery):
    global day, mouth, year
    day = callback.data.split('_')[-1]
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=create_inline_date_kb(day, mouth, year))
#Клавиатура выбора месяца
@router.callback_query(Text(text='month_btn'))
async def calendar_mouth_process(callback: CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=create_inline_month_kb())

#Выбираем месяц
@router.callback_query(Text(startswith='mounth_'))
async def calendar_choice_day_procces(callback: CallbackQuery):
    global day, mouth, year
    mouth = callback.data.split('_')[-1]
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=create_inline_date_kb(day, mouth, year))


#Клавиатура выбора года
@router.callback_query(Text(text='year_btn'))
async def calendar_mouth_process(callback: CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=create_inline_year_kb(year))

#Выбираем год
@router.callback_query(Text(startswith='year_'))
async def calendar_choice_day_procces(callback: CallbackQuery):
    global day, mouth, year
    year = callback.data.split('_')[-1]
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=create_inline_date_kb(day, mouth, year))


@router.callback_query(Text(text='ok'))
async def order_quantity_process(callback: CallbackQuery, state: FSMContext):
    global day, mouth, year
    await state.update_data(data_order=f'{day}/{mouth}/{year}')
    categ = await state.get_data()
    if categ['category'] == 'cakes':
        await callback.message.answer(text='Сколько килограмм торта Вы хотите?')
    elif categ['category'] == 'cupcakes' or categ['category'] == 'Cake_to_go':
        await callback.message.answer(text='Какое количество вы хотите?')
    elif categ['category'] == 'bento_cake':
        await callback.message.answer(text='Укажите диаметр бенто-торта? (10-14см)')

    await callback.answer()
    await state.set_state(FSMorder.quantity)


@router.message(StateFilter(FSMorder.quantity))#
async def order_filling_process(message: Message, state: FSMContext):
    await state.update_data(quantity=message.text)
    await message.answer(text='Загрузите фото образца торта\n'
                              'или опишите его')
    await state.set_state(FSMorder.decor)

#Фото торта\


@router.message(StateFilter(FSMorder.decor), F.photo[-1].file_id.as_("photo_id"), F.media_group_id.as_("album_id"))
async def collect_and_send_mediagroup(message: Message, photo_id: str, album_id: int, state: FSMContext):
    global new_album
    if album_id in mediagroups:
        mediagroups[album_id].append(photo_id)
        return
    mediagroups[album_id] = [photo_id]

    new_album = [InputMediaPhoto(media=file_id) for file_id in mediagroups[album_id]]
    await state.update_data(decor=new_album)
    await message.answer(text='Укажите способ достаки?\n'
                              'Самомывоз или доставка яндекс курьером', reply_markup=create_inline_kb(2, LEXICON_RU['method_pickup'], LEXICON_RU['method_delivery']))
    await state.set_state(FSMorder.delivery)


@router.message(StateFilter(FSMorder.decor), F.photo[-1].as_('largest_photo'))
async def order_decor_process(message: Message, state: FSMContext):
    await state.update_data(decor=message.photo[0].file_id)
    await message.answer(text='Укажите способ достаки?\n'
                              'Самомывоз или доставка яндекс курьером', reply_markup=create_inline_kb(2, LEXICON_RU['method_pickup'], LEXICON_RU['method_delivery']))
    await state.set_state(FSMorder.delivery)

#Описание торта
@router.message(StateFilter(FSMorder.decor))
async def warning_not_photo(message: Message, state: FSMContext):
    await state.update_data(decor=message.text)
    await message.answer(text='Укажите способ достака?\n'
                              'Самомывоз или доставка яндекс курьером', reply_markup=create_inline_kb(2, LEXICON_RU['method_pickup'], LEXICON_RU['method_delivery']))
    await state.set_state(FSMorder.delivery)

#Завершение заказа
@router.callback_query(Text(text=(LEXICON_RU['method_pickup'], LEXICON_RU['method_delivery'])), StateFilter(FSMorder.delivery))
async def order_delivery_process(callback: CallbackQuery, state: FSMContext):
    await state.update_data(delivery=callback.data)
    if callback.data == LEXICON_RU['method_pickup']:
        await callback.message.answer(text='Спасибо за заказ.\n'
                                    'В ближайшее время я с Вами свяжусь\n'
                                    'Адресс самовывоза: г. Балашиха, мкр. Гагарина д. 31, \n')
    else:
        await callback.message.answer(text='Спасибо за заказ.\n'
                                           'В ближайшее время я с Вами свяжусь\n'
                                           'Доставка осуществляется Яндекс курьером\n')
    await callback.answer()
    order_product = await state.get_data()
    if isinstance(order_product['decor'], str):
        if len(order_product['decor']) < 15 or len(str(order_product['decor']).split(' ')) > 1:
            await bot.send_message(654222332, text=f'Имя: {order_product["name_user"]}\n'
                                                   f'Контактный телефон: {order_product["telephon"]}\n'
                                                   f'Дата заказа: {order_product["data_order"]}\n'
                                                   f'Количество: {order_product["quantity"]}\n'
                                                   f'Декор: {order_product["decor"]}\n'
                                                   f'Способ доставки: {order_product["delivery"]}\n')
        else:
            await bot.send_photo(654222332, photo= order_product["decor"], caption=f'Имя: {order_product["name_user"]}\n'
                                                   f'Контактный телефон: {order_product["telephon"]}\n'
                                                   f'Дата заказа: {order_product["data_order"]}\n'
                                                   f'Количество: {order_product["quantity"]}\n'
                                                   f'Способ доставки: {order_product["delivery"]}\n')
    else:
        global new_album
        await bot.send_media_group(chat_id=f'{654222332}', media=new_album)
        await bot.send_message(654222332, text=f'Имя: {order_product["name_user"]}\n'
                                               f'Контактный телефон: {order_product["telephon"]}\n'
                                               f'Дата заказа: {order_product["data_order"]}\n'
                                               f'Количество: {order_product["quantity"]}\n'
                                               f'Способ доставки: {order_product["delivery"]}\n')
    await state.clear()




@router.message(Command(commands=['cancel']), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего. Вы не начинали оформление заказа')


@router.message(Command(commands=['cancel']), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Вы отказались от совершения заказа')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()
