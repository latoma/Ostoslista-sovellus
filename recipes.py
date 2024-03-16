from db import db
import users
from flask import session
from sqlalchemy.sql import text

# Adds new recipe to database and stores its id in session
def new(recipe_name):
    user_id = users.user_id()

    try:
        sql = text('INSERT INTO recipes (recipe_name, user_id) VALUES (:recipe_name, :user_id) RETURNING recipe_id')
        result = db.session.execute(sql, {"recipe_name":recipe_name, "user_id":user_id})
        db.session.commit()
    except:
        return False

    recipe_id = result.fetchone()[0]
    set_session_recipe_id(recipe_id)

    return True

def set_session_recipe_id(recipe_id):
    session["active_recipe_id"] = recipe_id

def session_recipe_id():
    return session.get("active_recipe_id")

def delete_session_recipe_id():
    if session_recipe_id():
        del session["active_recipe_id"]

# Get active recipe's name
def get_recipe_name():
    try:
        sql = text('SELECT recipe_name FROM recipes WHERE recipe_id = :recipe_id')
        result = db.session.execute(sql, {"recipe_id": session_recipe_id()})
        name = result.fetchone()
    except :
        return None

    return name[0] if name else None

# Returns all user recipes as list of recipe dictionaries
def get_recipes_with_items():
    result = ""
    try:
        sql = text('''
            SELECT r.recipe_id, r.recipe_name, ri.item_desc
            FROM recipes r
            LEFT JOIN recipe_items ri ON r.recipe_id = ri.recipe_id
            WHERE r.user_id = :user_id
        ''')
        result = db.session.execute(sql, {"user_id": users.user_id()})
    
    except:
        return None

    recipes = {}
    for row in result.fetchall():
        recipe_id, recipe_name, item_desc = row
        if recipe_id not in recipes:
            recipes[recipe_id] = {'recipe_name': recipe_name, 'recipe_id':recipe_id, 'recipe_items': []}
        if item_desc:
            recipes[recipe_id]['recipe_items'].append({'item_desc': item_desc})

    # Convert the dictionary of recipes into a list of recipe dictionaries.
    return list(recipes.values())

# Returns active recipe's items
def get_recipe_items():
    if session_recipe_id() == 0:
            return None
    try:
        sql = text('SELECT item_desc, item_id FROM recipe_items WHERE recipe_id =:recipe_id')
        result = db.session.execute(sql, {"recipe_id": session_recipe_id()})
        items = result.fetchall()
    except:
        return None
    
    return items    

# Adds item to active recipe
def add_item(item_desc):    
    try:
        sql = text("INSERT INTO recipe_items (recipe_id, item_desc) VALUES (:recipe_id, :item_desc)")
        db.session.execute(sql, {"recipe_id": session_recipe_id(), "item_desc": item_desc})
        db.session.commit()
    except:
        return False
    
    return True

# Delete recipe and its items from database
def delete_recipe():
        recipe_id = session_recipe_id()
        try:
            sql_items = text("DELETE FROM recipe_items WHERE recipe_id =:recipe_id")
            sql_list = text("DELETE FROM recipes WHERE recipe_id = :recipe_id AND user_id =:user_id")
            db.session.execute(sql_items, {"recipe_id": recipe_id})
            db.session.execute(sql_list, {"recipe_id": recipe_id, "user_id":users.user_id()})
            db.session.commit()
        except:
            return False
        
        return True
        
# Removes given list of items from database
def remove_items(item_ids):
    try:
        sql = text("DELETE FROM recipe_items WHERE item_id = ANY(:item_ids) AND recipe_id =:recipe_id")
        db.session.execute(sql, {"item_ids": item_ids, "recipe_id": session_recipe_id()})
        db.session.commit()
    except:
        return False
    
    return True

# Checks if user has access to given recipe
def has_access_to_recipe(recipe_id):
    try:
        sql = text('''
            SELECT EXISTS (
                SELECT 1
                FROM recipes
                WHERE recipe_id = :recipe_id AND user_id = :user_id
            )
        ''')
        result = db.session.execute(sql, {"recipe_id": recipe_id,
                                          "user_id": users.user_id()})
        access = result.fetchone()[0]

        if access:
            return True 
        
        return False
    except:
        return False