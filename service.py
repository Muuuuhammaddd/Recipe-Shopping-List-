from connection import connection




async def add_recipe(title_recipe):
    try:
        conn = await connection()
        avkot = await conn.execute("""
            INSERT INTO recipes(title_recipe) 
            VALUES ($1)
            """,title_recipe )
        return avkot
    except Exception as error:
        print(f"problem add_recipe: {error}")    
    finally:
        await conn.close()    

async def add_ingredients(recipe_id, name, cnt):
    try:
        conn = await connection()
        ingridiento = await conn.execute("""
            INSERT INTO ingredients(recipe_id, name_ingrid, amount) 
            VALUES ($1, $2, $3)
            """, int(recipe_id), str(name), int(cnt))
        return ingridiento
    except Exception as error:
        print(f"problem add_ingredient: {error}")    
    finally:
        await conn.close()   



async def show_recipe(title_recipe):
    try:
        conn = await connection()
        show = await conn.fetch("""
                SELECT * FROM recipes 
                JOIN ingredients ON recipes.recipe_id = ingredients.recipe_id
                WHERE recipes.title_recipe = $1
                """, f"{title_recipe}")
        return show
    except Exception as error:
        print(f"problem show_recipe_with_ingredients: {error}")    
    finally:
        await conn.close()



async def show_all_recipe():
    try:
        conn = await connection()
        show = await conn.fetch("SELECT * FROM recipes",)
        return show
    except Exception as error:
        print(f"problem show_all: {error}")    
    finally:
        await conn.close()



async def find_recipe(recipe_id):
    try:
        conn = await connection()
        recipe = await conn.fetchrow("""
            SELECT * FROM recipes WHERE recipe_id = $1
            """, int(recipe_id))
        return recipe
    except Exception as error:
        print(f"problem find_recipe: {error}")    
    finally:
        await conn.close()




async def add_plan(user_id, day_week, recipe_id):
    try:
        conn = await connection()
        plan = await conn.execute("""
            INSERT INTO meal_plan(user_id, day_of_week, recipe_id)
            VALUES ($1, $2, $3)
            """, str(user_id), str(day_week), int(recipe_id))
        return plan
    except Exception as error:
        print(f"problem add_plan: {error}")    
    finally:
        await conn.close()



async def get_shopping_list(user_id):
    try:
        conn = await connection()
        shopping_list = await conn.fetch("""
            SELECT meal_plan.day_of_week, recipes.title_recipe, ingredients.name_ingrid, ingredients.amount
            FROM meal_plan
            JOIN recipes ON meal_plan.recipe_id = recipes.recipe_id
            JOIN ingredients ON recipes.recipe_id = ingredients.recipe_id
            WHERE meal_plan.user_id = $1
            """, str(user_id))
        return shopping_list
    except Exception as error:
        print(f"problem get_shopping_list: {error}")    
    finally:
        await conn.close()      