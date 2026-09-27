import asyncpg
import os
from dotenv import load_dotenv
from mukimov.color import green, blue

async def connection():
    try:
        conn = await asyncpg.connect(
            database="recipe_shopping_db",
            host="localhost",
            user="postgres",
            port=5432,
            password=os.getenv("password_db")
        )
        print(blue('connect OK'))
        return conn
    except Exception as error:
        print(f"connect error: {error}")


async def create_table():
    conn = await connection()
    try:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS recipes(
                recipe_id serial primary key,
                title_recipe varchar(100)
            );
            CREATE TABLE IF NOT EXISTS ingredients(
                ingredient_id serial primary key,
                recipe_id int references recipes(recipe_id),
                name_ingrid varchar(100),
                amount int
            );

            CREATE TABLE IF NOT EXISTS meal_plan(
                plan_id serial primary key,
                user_id text,
                day_of_week smallint,
                recipe_id int references recipes(recipe_id)
            );
        """)
        print(green('Tables Created!'))
    except Exception as error:
        print(f"create table error: {error}")
    finally:
        await conn.close()