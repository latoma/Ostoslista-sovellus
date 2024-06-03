from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
import shopping_lists, recipes
import base64


# SECURITY LOGGING AND MONITORING FAILURE:
# No login threat detection
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
        
# FIX:
# # Define a dictionary to store login attempts
# login_attempts = {}

# # Define constants for login attempt thresholds and lockout duration
# MAX_LOGIN_ATTEMPTS = 5
# LOCKOUT_DURATION_MINUTES = 15
# ...
# # Logic is something like this:
#
# # Check if the user is currently locked out due to previous failed attempts
# if username in login_attempts and login_attempts[username]['locked']:
#     if login_attempts[username]['lockout_time'] > datetime.now():
#         # User is still locked out
#         return False
#     else:
#         # Lockout period has expired, reset login attempts
#         login_attempts[username]['attempts'] = 0
#         login_attempts[username]['locked'] = False

def logout():
    del session["user_id"]
    shopping_lists.delete_session_list_id()
    recipes.delete_session_recipe_id()

def register(username, password):
    # BAD HASHING
    hash_value = base64.b64encode(password.encode()).decode();
    # FIX:
    # hash_value = generate_password_hash(password)
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