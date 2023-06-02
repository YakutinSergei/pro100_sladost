from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lexicon.lexicon_ru import LEXICON_RU


btn_add: KeyboardButton = KeyboardButton(text=LEXICON_RU['btn_add'])
btn_del: KeyboardButton = KeyboardButton(text='Удалить')
admin_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[btn_add],[btn_del]],
                                                    resize_keyboard=True)