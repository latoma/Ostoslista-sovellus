from db import db
import users
from flask import session
from sqlalchemy.sql import text

def new(recipe_name):
    user_id = users.user_id()
    if user_id == 0:
        return False
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

def get_recipe_name():
    try:
        sql = text('SELECT recipe_name FROM recipes WHERE recipe_id = :recipe_id')
        result = db.session.execute(sql, {"recipe_id": session_recipe_id()})
        name = result.fetchone()
        if name:
            return name[0]
        else:
            return False
    except :
        return False
    
def add_item(item_desc):
    if users.user_id() == 0:
        return False
    
    try:
        sql = text("INSERT INTO recipe_items (recipe_id, item_desc) VALUES (:recipe_id, :item_desc)")
        db.session.execute(sql, {"recipe_id": session_recipe_id(), "item_desc": item_desc})
        db.session.commit()
    except:
        return False
    
    return True

def get_recipe_items():
    if session_recipe_id() == 0:
            return None
    try:
        sql = text('SELECT item_desc, item_id FROM recipe_items WHERE recipe_id =:recipe_id')
        result = db.session.execute(sql, {"recipe_id": session_recipe_id()})
        items = result.fetchall()
        return items
    except:
        return None
    
def get_recipes():
    result = ""
    try:
        sql = text('''
            SELECT r.recipe_id, r.recipe_name, ri.item_desc
            FROM recipes r
            LEFT JOIN recipe_items ri ON r.recipe_id = ri.recipe_id
            WHERE r.user_id = :user_id
        ''')
        result = db.session.execute(sql, {"user_id": users.user_id()})
    
    except Exception as e:
        print("Error fetching recipes:", e)
        return None

    recipes = {}
    for row in result.fetchall():
        recipe_id, recipe_name, item_desc = row
        if recipe_id not in recipes:
            recipes[recipe_id] = {'recipe_name': recipe_name, 'recipe_id':recipe_id, 'recipe_items': []}
        if item_desc:
            recipes[recipe_id]['recipe_items'].append({'item_desc': item_desc})

    return list(recipes.values())

def delete_session_recipe_id():
    if session_recipe_id():
        del session["active_recipe_id"]

def delete_recipe():
        id = session_recipe_id()
        try:
            sql_items = text("DELETE FROM recipe_items WHERE recipe_id =:recipe_id")
            sql_list = text("DELETE FROM recipes WHERE recipe_id = :recipe_id AND user_id =:user_id")

            db.session.execute(sql_items, {"recipe_id": id})
            db.session.execute(sql_list, {"recipe_id": id, "user_id":users.user_id()})
            db.session.commit()
            return True
        except:
            return False
        
# Removes given item_id(s) from database
def remove_items(item_ids):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try:
        sql = text("DELETE FROM recipe_items WHERE item_id = ANY(:item_ids)")
        db.session.execute(sql, {"item_ids": item_ids})
        db.session.commit()
    except:
        return False
    
    return True

