from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message
from keyboards.keyboards import  order_kb, order_select_kb
from lexicon.lexicon_ru import LEXICON_RU
from create_bot import bot
router: Router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=order_kb)



# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=order_kb)


# Этот хэндлер срабатывает на кнопку Заказать
@router.message(Text(text=LEXICON_RU['order']))
async def process_yes_answer(message: Message):
    await bot.send_message(message.from_user.id, text=LEXICON_RU['order_select'], reply_markup=order_select_kb)

