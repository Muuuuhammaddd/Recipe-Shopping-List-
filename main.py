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
    await message.answer(f"==Вы добавили==:\n ID-Рецептa: {ingred[0]}\n Ингридиет {ingred[1]}!\n Каличество: {ingred[2]}-кг\n\n")

@dp.message(F.text == '📖 Мои рецепты')
async def all_resipe(message: Message):
    all = await show_all_recipe()
    txt = 'Репецты пуста\n\n'
    for i in all:
        txt += f'ID: {i['recipe_id']} | Названия Рецепта: {i['title_recipe']}\n'
    await message.answer(txt)




@dp.message(Command('show_list'))
async def show(message: Message, command: CommandObject):
    recipe_title = command.args
    result = await show_recipe(recipe_title)
    if not result:
        await message.answer("Рецепт не найден")
        return
    txt = 'Рецепты c игридиентамы!\n\n'
    for i in result:
        txt += f'Названия Рецепта: {i['title_recipe']}\nИнгридиенты: {i['name_ingrid']}\nКоличевства: {i['amount']}кг\n\n'
    await message.answer(txt)



@dp.message(Command('plan'))
async def plans(message: Message, command: CommandObject):
    num = command.args.split(',')
    day_week = num[0].strip()
    recipe_id = num[1].strip()

    await add_plan(message.from_user.id, day_week, recipe_id)
    name = await find_recipe(int(recipe_id))
    await message.answer(F'PLAN ADDED!!!\n\nUSER NAME: {message.from_user.full_name}\nDay Week: {day_week}\nRECIPE NAME:{name['title_recipe']}')



@dp.message(F.text == '🛒 Список покупок')
@dp.message(Command('shopping_list'))
async def shopping_list(message: Message):
    result = await get_shopping_list(message.from_user.id)

    if not result:
        await message.answer("Ваш план питания пуст")
        return

    text = f"🛒 Список покупок для @{message.from_user.username}:\n\n"
    for i in result:
        text += f"{i['day_of_week']}\n • {i['title_recipe']} • {i['name_ingrid']}: • {i['amount']}кг\n\n"

    await message.answer(text)



@dp.message()
async def start(message: Message):
    await message.answer(f'Точики гап зан!')

async def main():
    print(green('BOT РАБОТАЕТ!!!'))

    await create_table()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())