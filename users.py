from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
import shopping_lists, recipes

def login(username, password):
    sql = text('SELECT user_id, password FROM users WHERE username=:username')
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.user_id
            session["username"] = username
            return True
        else:
            return False

def logout():
    del session["user_id"]
    shopping_lists.delete_session_list_id()
    recipes.delete_session_recipe_id()

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username,password) VALUES (:username,:password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id", 0)

def session_username():
    return session.get("username", 0)

# Checks if username exists in database
def username_in_database(username):
    try:
        sql = text('SELECT COUNT(*) FROM users WHERE username=:username')
        result = db.session.execute(sql, {"username": username})
        count = result.scalar()
    except:
        return False
    return count > 0