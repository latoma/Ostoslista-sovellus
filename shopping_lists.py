from db import db
import users
from flask import session
from sqlalchemy.sql import text


def new(list_name):
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = text('INSERT INTO shopping_lists (list_name, user_id) VALUES (:list_name, :user_id) RETURNING list_id')
    result = db.session.execute(sql, {"list_name":list_name, "user_id":user_id})
    db.session.commit()

    # The new list's id is saved to the session
    set_active_list_id(result.fetchone()[0])

    return True

def set_active_list_id(list_id):
    session["active_list_id"] = list_id

def active_list_id():
    return session.get("active_list_id")

def delete_active_list_id():
    del session["active_list_id"]

def get_list_name():
    try:
        sql = text("SELECT list_name FROM shopping_lists WHERE list_id = :list_id")
        result = db.session.execute(sql, {"list_id" : active_list_id()})
        list = result.fetchone()

    except:
        return False
    
    return list

# Returns the content behind session["list_id"]
def get_items():
    list_id = active_list_id()
    sql = text("SELECT item_desc, item_id FROM item_lists WHERE list_id = :list_id")
    result = db.session.execute(sql, {"list_id": list_id})
        
    return result.fetchall()

def add_item(item_desc):
    user_id = users.user_id()
    list_id = active_list_id()
    if user_id == 0:
        return False
    
    sql = text("INSERT INTO item_lists (list_id, item_desc) VALUES (:list_id, :item_desc)")
    db.session.execute(sql, {"list_id": list_id, "item_desc": item_desc})
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

def get_shopping_lists():
    try:
        sql = text("SELECT list_name, list_id FROM shopping_lists WHERE user_id = :user_id ")
        result = db.session.execute(sql, {"user_id" : users.user_id()})
        lists = result.fetchall()
    except:
        return False
    return lists

def delete_list():
    list_id = active_list_id()
    try:
        sql_items = text("DELETE FROM item_lists WHERE list_id =:list_id")
        sql_list = text("DELETE FROM shopping_lists WHERE list_id = :list_id")

        db.session.execute(sql_items, {"list_id": list_id})
        db.session.execute(sql_list, {"list_id": list_id})
        db.session.commit()
    except:
        return False
    
    delete_active_list_id()
    return True