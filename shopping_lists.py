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

# Shares active list to given user_id
def share_list(username):
    try:
        sql = text('INSERT INTO shared_lists (list_id, username) VALUES (:list_id, :username)')
        db.session.execute(sql, {"list_id": session_list_id(), "username": username})
        db.session.commit()
    except:
        return False
    return True

# Query the database to get the usernames of users with whom the list is shared with
def get_shared_users():
    try:
        sql = text('SELECT username FROM shared_lists WHERE list_id = :list_id')
        result = db.session.execute(sql, {"list_id": session_list_id()})
        shared_users = [row[0] for row in result.fetchall()]

        # Join the usernames into a single string separated by commas
        shared_users_string = ", ".join(shared_users)

        return shared_users_string
    except:
        return None
    
def set_active_list_id(list_id):
    # Check if the user has access to the list
    if has_access_to_list(list_id):
        session["active_list_id"] = list_id
        return True
    else:
        return False

def session_list_id():
    return session.get("active_list_id")

def delete_session_list_id():
    if session_list_id():
        del session["active_list_id"]

def get_list_name():
    try:
        sql = text("SELECT list_name FROM shopping_lists WHERE list_id = :list_id")
        result = db.session.execute(sql, {"list_id" : session_list_id()})
        list = result.fetchone()

    except:
        return False
    if list:
        return list[0]
    else:
        return []

# Returns the content behind session["list_id"]
def get_items():
    list_id = session_list_id()
    sql = text("SELECT item_desc, item_id FROM list_items WHERE list_id = :list_id")
    result = db.session.execute(sql, {"list_id": list_id})
        
    return result.fetchall()

def add_item(item_desc):
    user_id = users.user_id()
    list_id = session_list_id()
    if user_id == 0:
        return False
    
    sql = text("INSERT INTO list_items (list_id, item_desc) VALUES (:list_id, :item_desc)")
    db.session.execute(sql, {"list_id": list_id, "item_desc": item_desc})
    db.session.commit()

    return True

# Removes given item_id(s) from database
def remove_items(item_ids):
    user_id = users.user_id()
    if user_id == 0:
        return False

    try:
        sql = text("DELETE FROM list_items WHERE item_id = ANY(:item_ids)")
        db.session.execute(sql, {"item_ids": item_ids})
        db.session.commit()
    
    except:
        return False

    return True

def get_shopping_lists():
    try:
        sql = text("SELECT list_name, list_id FROM shopping_lists WHERE user_id =:user_id")
        result = db.session.execute(sql, {"user_id" : users.user_id()})
        lists = result.fetchall()
    except:
        return None
    return lists

def delete_list():
    list_id = session_list_id()
    try:
        sql_items = text("DELETE FROM list_items WHERE list_id =:list_id")
        sql_list = text("DELETE FROM shopping_lists WHERE list_id =:list_id AND user_id=:user_id")

        db.session.execute(sql_items, {"list_id": list_id})
        db.session.execute(sql_list, {"list_id": list_id, "user_id": users.user_id()})
        db.session.commit()
    except:
        return False

# Checks if user has access to given list_id 
def has_access_to_list(list_id):
        try:
            sql = text("SELECT COUNT(*) FROM shopping_lists WHERE user_id = :user_id AND list_id = :list_id")
            result = db.session.execute(sql, {"user_id": users.user_id(), "list_id": list_id})
            count = result.scalar()  # Get the result as a single value

            # If count is greater than 0, the user has access to the list
            return count > 0
        except:
            return False
        