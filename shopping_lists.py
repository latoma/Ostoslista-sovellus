from db import db
import users
from flask import session
from sqlalchemy.sql import text

# Adds new list to database and stores it in session
def new(list_name):
    user_id = users.user_id()

    try:
        sql = text('''INSERT INTO shopping_lists (list_name, user_id, created_by) 
                   VALUES (:list_name, :user_id, :created_by) 
                   RETURNING list_id''')
        result = db.session.execute(sql, {"list_name":list_name, 
                                          "user_id":user_id,
                                          "created_by": users.session_username()})
        db.session.commit()

        # The new list's id is saved to the session
        set_session_list_id(result.fetchone()[0])

    except:
        return False

    return True
    
def set_session_list_id(list_id):
    session["active_list_id"] = list_id

def session_list_id():
    return session.get("active_list_id")

def delete_session_list_id():
    if session_list_id():
        del session["active_list_id"]

# Add item to database for active list
def add_item(item_desc):  
    try:
        list_id = session_list_id()
        sql = f"INSERT INTO list_items (list_id, item_desc) VALUES ({list_id}, '{item_desc}')"
        db.session.execute(sql)
        db.session.commit()
        
    except:
        return False
    
    return True

# Shares active list to given user_id
def share_list(username):
    try:
        # SQL-INJECTION FLAW
        # The user inputs are inserted into the SQL query directly, which enables query manipulation.
        sql = text(f'INSERT INTO list_items (list_id, username) VALUES ({session_list_id()}, "{username}")')
        db.session.execute(sql)
        # FIX (using parameterization):
        # sql = text("INSERT INTO list_items (list_id, item_desc) VALUES (:list_id, :item_desc)")
        # db.session.execute(sql, {"list_id": session_list_id(), "item_desc": item_desc})
        db.session.commit()
    except:
        return False
    return True

# Removes given item_id(s) from database
def remove_items(item_ids):
    try:
        sql = text("DELETE FROM list_items WHERE item_id = ANY(:item_ids)")
        db.session.execute(sql, {"item_ids": item_ids})
        db.session.commit()
    except:
        return False

    return True

# Returns list_name, created_by and created_at
def get_list_info():
    try:
        sql = text("SELECT list_name, created_by, created_at FROM shopping_lists WHERE list_id = :list_id")
        result = db.session.execute(sql, {"list_id" : session_list_id()})
        list = result.fetchone()

    except:
        return None
    
    return list

# Returns the list_items behind session list_id
def get_items():
    try:
        sql = text("SELECT item_desc, item_id FROM list_items WHERE list_id = :list_id")
        result = db.session.execute(sql, {"list_id": session_list_id()})
        return result.fetchall()
    except:
        return None


# Gives the lists that other users have shared
def get_shared_lists():
    try:
        sql_query = text('''
            SELECT sl.list_name, sl.list_id
            FROM shopping_lists AS sl
            JOIN shared_lists AS sls ON sl.list_id = sls.list_id
            JOIN users AS u ON sls.username = u.username
            WHERE u.user_id = :user_id
        ''')

        result = db.session.execute(sql_query, {"user_id": users.user_id()})
        shared_lists = result.fetchall()

        return shared_lists
   
    except:
        return None
    
# Gives the usernames of users with whom the list is shared with
def get_shared_users():
    try:
        sql = text('SELECT username FROM shared_lists WHERE list_id = :list_id')
        result = db.session.execute(sql, {"list_id": session_list_id()})
        shared_users = [row[0] for row in result.fetchall()]

        return shared_users
    except:
        return None

# Gives all shopping lists the user has made
def get_shopping_lists():
    try:
        sql = text("SELECT list_name, list_id FROM shopping_lists WHERE user_id =:user_id")
        result = db.session.execute(sql, {"user_id" : users.user_id()})
        lists = result.fetchall()
    except:
        return None
    
    return lists

# Deletes list items, sharing and the list itself from database
def delete_list():
    list_id = session_list_id()
    user_id = users.user_id()

    try:
        sql_items = text("DELETE FROM list_items WHERE list_id =:list_id")
        db.session.execute(sql_items, {"list_id": list_id})

        sql_shared = text("DELETE FROM shared_lists WHERE list_id =:list_id")
        db.session.execute(sql_shared, {"list_id": list_id})

        sql_list = text("""DELETE FROM shopping_lists 
                        WHERE list_id =:list_id AND user_id=:user_id""")
        db.session.execute(sql_list, {"list_id": list_id, 
                                      "user_id": user_id})
        db.session.commit()
    except:
        return False
    
    return True

# Deletes user from shared users of active list
def delete_sharing():
    try:
        sql = text("""DELETE FROM shared_lists 
                   WHERE username=:username AND list_id=:list_id""")
        db.session.execute(sql, {"username": users.session_username(), 
                                 "list_id": session_list_id()})
        db.session.commit()
    except:
        return False
    return True

# Checks if user has access to given list_id 
def has_access_to_list(list_id):
    try:
        # Check access from shopping_lists
        sql_shopping = text('''
            SELECT EXISTS (
                SELECT 1
                FROM shopping_lists
                WHERE list_id = :list_id AND user_id = :user_id
            )
        ''')
        result = db.session.execute(sql_shopping, {"list_id": list_id, 
                                                   "user_id": users.user_id()})
        shopping_access = result.fetchone()[0]

        if shopping_access:
            return True 
        
        # Check acccess from shared_lists
        sql_shared = text('''
            SELECT EXISTS (
                SELECT 1
                FROM shared_lists
                WHERE list_id = :list_id
                AND username = (
                    SELECT username
                    FROM users
                    WHERE user_id = :user_id
                )
            )
        ''')
        result = db.session.execute(sql_shared, {"list_id": list_id, 
                                                 "user_id": users.user_id()})
        shared_access = result.fetchone()[0]

        if shared_access:
            return True
        
        return False 
    
    except:
        return False 
