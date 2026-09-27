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



async def show_recipe(recipe_id):
    try:
        conn = await connection()
        show = await conn.fetch("""
                SELECT * FROM recipes 
                JOIN ingredients ON recipes.recipe_id = ingredients.recipe_id
                WHERE recipes.recipe_id = $1
                """, int(recipe_id))
        
        return show
    except Exception as error:
        print(f"problem show_recipe_with_ingredients: {error}")    
    finally:
        await conn.close()  




    