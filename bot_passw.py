from config import token
from random import choice
from string import digits, ascii_uppercase, ascii_lowercase, punctuation
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=token)
dp = Dispatcher(bot)

def get_keyboard():
    buttons = [
        types.InlineKeyboardButton(text="Большие буквы", callback_data="num_upper"),
        types.InlineKeyboardButton(text="Маленькие буквы", callback_data="num_lower"),
        types.InlineKeyboardButton(text="Цифры", callback_data="num_digit"),
        types.InlineKeyboardButton(text="Символы", callback_data="num_symbol"),
        types.InlineKeyboardButton(text="Показать пароль", callback_data="num_finish")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


@dp.message_handler(commands='start')
async def pass_start(message: types.Message):
    await message.answer('Добро пожаловать в бот-генератор пароля')
    await message.answer('Сколько символов будет у пароля?')


@dp.message_handler()
async def length(message: types.Message):
    await message.answer('Из каких символов будет состоять пароль?', reply_markup=get_keyboard())
    global length_pass
    length_pass = int(message.text)
    return


list_symbol = []


@dp.callback_query_handler()
async def greate_password(call: types.CallbackQuery):
    await call.answer()

    action = call.data.split("_")[1]
    if action == 'upper':
        list_symbol.append(ascii_uppercase)
    if action == 'lower':
        list_symbol.append(ascii_lowercase)
    if action == 'digit':
        list_symbol.append(digits)
    if action == 'symbol':
        list_symbol.append(punctuation)
    if action == 'finish':
        if list_symbol:
            await call.message.delete_reply_markup()

            password = {choice(''.join(list_symbol)) for _ in range(length_pass)}
            if len(password) == length_pass and sum(bool(password & set(x)) for x in list_symbol) == len(
                    list_symbol):
                await call.message.answer(f"Ваш пароль:  {''.join(password)}")
                await call.message.answer('Хотите сгенерировать еще один пароль? Нажмите /start')

                list_symbol.clear()


if __name__ == '__main__':
    executor.start_polling(dp)