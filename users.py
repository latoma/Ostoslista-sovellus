from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

def login(username, password):
    sql = text('SELECT user_id, password FROM users WHERE username=:username')
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.user_id
            return True
        else:
            return False

def logout():
    del session["user_id"]

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
    return session.get("user_id",0)

def active_list_id():
    return session.get("list_id")

def get_shopping_lists():
    try:
        sql = text("SELECT list_name, list_id FROM shopping_lists WHERE user_id = :user_id ")
        result = db.session.execute(sql, {"user_id" : user_id()})
        lists = result.fetchall()
    except:
        return False
    return lists

def set_list_id(list_id):
    session["list_id"] = list_id
    
def get_list_name():
    try:
        sql = text("SELECT list_name FROM shopping_lists WHERE list_id = :list_id")
        result = db.session.execute(sql, {"list_id" : active_list_id()})
        list = result.fetchone()

    except:
        return False
    
    return list