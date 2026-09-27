import asyncio
from mukimov.color import green
from aiogram import Dispatcher, Bot, F
from dotenv import load_dotenv
import os
from connection import create_table
from service import *
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, CommandObject

load_dotenv()
bot = Bot(os.getenv("token_bot"))
dp = Dispatcher()
knopka = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📖 Мои рецепты")],
        [KeyboardButton(text="🛒 Список покупок")],
    ], 
    resize_keyboard=True
)





@dp.message(Command('start'))
async def start(message: Message):
    await message.answer(f"Hello  @{message.from_user.username}", reply_markup=knopka)
    
@dp.message(Command('add_recipe'))
async def recipes(message: Message, command: CommandObject):
    recipe = command.args
    await add_recipe(recipe)
    await message.answer(f"Вы добавили: {recipe}!")

@dp.message(Command('add_ingredient'))
async def ingredients(message: Message, command: CommandObject):
    ingred = command.args.split(',')
    await add_ingredients(ingred[0],ingred[1],ingred[2])
    await message.answer(f"Вы добавили: {ingred[1]}!\nКаличество: {ingred[2]}")



@dp.message(Command('show_list'))
async def show(message: Message, command: CommandObject):
    recipe_id = command.args
    result = await show_recipe(int(recipe_id))
    if not result:
        await message.answer("Рецепт не найден")
        return
    txt = 'Рецепты c игрыдиентамы!\n\n'
    for i in result:
        txt += f'Resipe Name: {i['title_recipe']}\nIngredient: {i['name_ingrid']}\nAmout: {i['amount']}\n\n'
    await message.answer(txt)


@dp.message()
async def start(message: Message):
    await message.reply_to_message(f'Точики гап зан!')

async def main():
    print(green('BOT РАБОТАЕТ!!!'))

    await create_table()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())