from db import db
import users
from flask import session
from sqlalchemy.sql import text
from datetime import datetime

def get_list():
    sql = text('')

def new():
    user_id = users.user_id()
    if user_id == 0:
        return False
    
    # Generates name for the list
    current_date = datetime.now()
    formatted_date = current_date.strftime('%d/%m/%Y')
    list_name = "Ostoslista " + formatted_date

    sql = text('INSERT INTO shopping_lists (list_name, user_id) VALUES (:list_name, :user_id) RETURNING list_id')
    result = db.session.execute(sql, {"list_name":list_name, "user_id":user_id})
    db.session.commit()

    # The new list's id is saved to the session
    session["list_id"] = result.fetchone()[0]

    return True

# Returns the content behind session["list_id"]
def get_items():
    sql = text("SELECT item_desc, item_id FROM item_lists WHERE list_id = :list_id")
    result = db.session.execute(sql, {"list_id": session.get("list_id")})
        
    return result.fetchall()

def add_item(item_desc):
    user_id = users.user_id()
    if user_id == 0:
        return False
    
    sql = text("INSERT INTO item_lists (list_id, item_desc) VALUES (:list_id, :item_desc)")
    db.session.execute(sql, {"list_id": session.get("list_id"), "item_desc":item_desc})
    db.session.commit()

    return True

# Removes given item_id(s) from database
def remove_items(item_ids):
    user_id = users.user_id()
    if user_id == 0:
        return False
    
    if isinstance(item_ids, int):
        sql = text("DELETE FROM item_lists WHERE item_id = :item_ids")
    elif isinstance(item_ids, list):
        sql = text("DELETE FROM item_lists WHERE item_id = ANY(:item_ids)")
    
    db.session.execute(sql, {"item_ids": item_ids})
    db.session.commit()

    return True