from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from keyboards.keyboards import  order_kb, order_select_kb, create_pagination_keyboard
from lexicon.lexicon_ru import LEXICON_RU
from create_bot import bot
from data_base.sqlite_bd import sql_read, append_categor, append_res, append_pg

router: Router = Router()

# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=order_kb)




# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=order_kb)


#При нажатии на меню
@router.message(Text(text=LEXICON_RU['menu']))
async def procces_menu_command(message: Message):
    await message.answer(text='Выбирите категорию', reply_markup=order_select_kb)


# Этот хэндлер срабатывает на кнопку Заказать
@router.message(Text(text=LEXICON_RU['order']))
async def process_yes_answer(message: Message):
    await bot.send_message(message.from_user.id, text=LEXICON_RU['order_select'], reply_markup=order_select_kb)


@router.callback_query(Text(text='forward'))
async def process_forward_press(callback: CallbackQuery):
    pg = append_pg(0)
    res = append_res()
    len_pg = len(res)
    print(res)
    if pg+1 < len_pg:
        pg = append_pg(+1)
        await bot.edit_message_media(
                                    chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id,
                                    media=InputMediaPhoto(media=res[pg][1],
                                                                caption=f'{res[pg][2]}\nОписание: {res[pg][3]}\n Цена:{res[pg][-1]}'),
                                   reply_markup=create_pagination_keyboard('backward',
                                     f'{pg+1}/{len_pg}',
                                    'forward'))
    await callback.answer()
@router.callback_query(Text(text='backward'))
async def process_forward_press(callback: CallbackQuery):
    pg = append_pg(0)
    res = append_res()
    len_pg = len(res)
    if pg > 0:
        pg = append_pg(-1)
        if pg < len_pg:
            await bot.edit_message_media(
                                    chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id,
                                            media=InputMediaPhoto(media=res[pg][1],
                                                                    caption=f'{res[pg][2]}\nОписание: {res[pg][3]}\n Цена:{res[pg][-1]}'),
                                           reply_markup=create_pagination_keyboard('backward',
                                             f'{pg+1}/{len_pg}',
                                            'forward'))
    await callback.answer()


#Кнопка назад
@router.callback_query(Text(text='назад'))
async def back_category_command(callback: CallbackQuery):
    await callback.message.answer(text='Выбирите категорию', reply_markup=order_select_kb)
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.answer()

@router.callback_query()
async def print_user_categoryes_cammand(callback: CallbackQuery):
    res = await sql_read('btn_admin_'+callback.data)
    pg = append_pg(0)
    len_pg = len(res)
    if len_pg > 0:
        await bot.send_photo(chat_id=callback.from_user.id, photo=res[pg][1],
                             caption=f'{res[pg][2]}\nОписание: {res[pg][3]}\n Цена:{res[pg][-1]}',
                             reply_markup=create_pagination_keyboard('backward',
                                                                           f'{pg + 1}/{len_pg}',
                                                                           'forward'))
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.answer()

