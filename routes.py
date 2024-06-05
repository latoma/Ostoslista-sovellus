from app import app
from flask import render_template, request, redirect, session, abort
import users, shopping_lists, recipes, secrets
from datetime import datetime
from functools import wraps

# # CSRF FIX:
# # A wrapper function:
# # Performs CSRF token verification for POST methods and validates user
# def check_user_required(view_func):
#     @wraps(view_func)
#     def decorated_function(*args, **kwargs):
#         csrf_token = (request.form.get('csrf_token') 
#               if request.method == 'POST' 
#               else None)

#         if csrf_token and session.get('csrf_token') != csrf_token:
#             abort(403)

#         if users.user_id() == 0:
#             abort(403)

#         return view_func(*args, **kwargs)

#     return decorated_function

@app.route("/")
def index():
    if users.user_id() == 0:
        return render_template("index.html")
    else:
        return render_template("index.html", 
                               lists = shopping_lists.get_shopping_lists(), 
                               recipe_list = recipes.get_recipes_with_items(),
                               shared_lists = shopping_lists.get_shared_lists())

@app.route("/list")
def list():
    shared = shopping_lists.get_shared_users()
    if shared:
        return render_template("list.html", 
                               list = shopping_lists.get_list_info(),
                               shared_to = ",".join(shared), 
                               items = shopping_lists.get_items(), 
                               recipe_list = recipes.get_recipes_with_items())
    else:
        return render_template("list.html", 
                               list = shopping_lists.get_list_info(), 
                               items = shopping_lists.get_items(), 
                               recipe_list = recipes.get_recipes_with_items())
    
@app.route("/new_list", methods=['GET', 'POST'])
# @check_user_required
def new_list():
    if request.method == "GET":
        return render_template("new_list.html")

    if request.method == "POST":
        list_name = request.form["list_name"]
        print(len(list_name))
        if 3 <= len(list_name) <= 40:
            if shopping_lists.new(list_name):
                return redirect("/list")
            else:
                return render_template("error.html", message="Listan muodostaminen epäonnistui")
        else:
            return render_template("error.html", message="Nimen pituus on oltava 3-40 merkkiä pitkä")

@app.route("/add_list_item", methods=["POST"])
def add_item():
    if request.method == "POST":
        item_desc = request.form["content"]
        if 3 <= len(item_desc) <= 40:
            if shopping_lists.add_item(item_desc):
                return redirect("/list")
            else:
                return  render_template("error.html", message="Tuotteen lisääminen ei onnistunut")
        else:
            return render_template("error.html", message="Nimen pituus on oltava 3-40 merkkiä pitkä")

@app.route("/remove_list_items", methods=["POST"])
# @check_user_required
def remove_list_items():
    if request.method == "POST":
        removed_item_ids_string = request.form.get('removedItems')
        if removed_item_ids_string is not None and removed_item_ids_string != "":
            removed_item_ids = [int(x) for x in removed_item_ids_string.split(",")]
            shopping_lists.remove_items(removed_item_ids)

        return redirect("/list")

# Activates list in session
# If GET, it just shows the list
# If POST, it redirects to editing mode                     
@app.route("/activate_list", methods=["GET", "POST"])
def activate_list():
    if request.method == "GET":
        list_id = request.args.get('list_id')
        if shopping_lists.has_access_to_list(list_id):
            shopping_lists.set_session_list_id(list_id)
            return render_template("show_list.html", 
                                   list = shopping_lists.get_list_info(), 
                                   items = shopping_lists.get_items())
        
    if request.method == "POST":    
        list_id = request.form["list_id"]
        if shopping_lists.has_access_to_list(list_id):
            shopping_lists.set_session_list_id(list_id)            
            return redirect("/list")
    
    return render_template("error.html", message="Ei oikeutta listaan")    


    
@app.route("/share_list", methods=["GET", "POST"])
# @check_user_required
def share_list():
    if request.method == "GET":
        return render_template("share.html")

    if request.method == "POST":
        username = request.form["username"].strip()
        state = False
        message = ""

        if username == users.session_username():
            message = "Et voi jakaa itsellesi!"

        elif not users.username_in_database(username):
            message = f"Käyttäjää {username} ei löytynyt!"

        elif username in shopping_lists.get_shared_users():
            message = f"Lista on jo jaettu käyttäjälle {username}!"

        else: 
            state = shopping_lists.share_list(username)
            if state:
                message = f"Jakaminen käyttäjälle {username} onnistui!"
            else:
                message = "SQL virhe"
            
        return render_template("share.html", 
                               success = state,
                               message = message)
        
@app.route("/delete_list", methods=["POST"])
# @check_user_required
def delete_list():
    if request.method == "POST":
        shared = shopping_lists.get_shared_users()
        if shared:
            if shopping_lists.delete_sharing():
                return redirect("/")                
        
        else:
            if shopping_lists.delete_list():
                return redirect("/")
        
        return render_template("error.html", message="Listan poistaminen epäonnistui")
   
@app.route("/recipe")
def recipe():
    return render_template("recipe.html", 
                           recipe_name = recipes.get_recipe_name(), 
                           items = recipes.get_recipe_items())

@app.route("/new_recipe", methods=['GET', 'POST'])
# @check_user_required
def new_recipe():
    if request.method == "GET":
        return render_template("new_recipe.html")

    if request.method == "POST":
        recipe_name = request.form["recipe_name"]
        if 3 <= len(recipe_name) <= 40:
            if recipes.new(recipe_name):
                return redirect("/recipe")
            else:
                return render_template("error.html", message="Reseptin muodostaminen ei onnistunut")
        else:
            return render_template("error.html", message="Nimen pituus on oltava 3-40 merkkiä pitkä")
        
@app.route("/add_recipe_item", methods=["POST"])
def add_recipe_item():
    if request.method == "POST":
        item_desc = request.form["content"]
        if 3 <= len(item_desc) <= 40:
            if recipes.add_item(item_desc):
                    return redirect("/recipe")
            else:
                return render_template("error.html", message="Tuotteen lisääminen ei onnistunut")
        else:
            return render_template("error.html", message="Nimen pituus on oltava 3-40 merkkiä pitkä")


@app.route("/remove_recipe_items", methods=["POST"])
# @check_user_required
def remove_recipe_items():
    if request.method == "POST":
        removed_item_ids_string = request.form.get('removedItems')
        if removed_item_ids_string is not None and removed_item_ids_string != "":
            removed_item_ids = [int(x) for x in removed_item_ids_string.split(",")]
            recipes.remove_items(removed_item_ids)

        return redirect("/recipe")        
        
@app.route("/activate_recipe", methods=['POST'])
# @check_user_required
def activate_recipe():
    if request.method == 'POST':
        recipe_id = request.form["recipe_id"]
        if recipes.has_access_to_recipe(recipe_id):
            recipes.set_session_recipe_id(recipe_id)
            return redirect("/recipe")
        else:
            render_template("error.html", message="Ei oikeutta reseptiin",)

@app.route("/delete_recipe", methods=["POST"])
# @check_user_required
def delete_recipe():
    if request.method == "POST":
        if recipes.delete_recipe():
            return redirect("/")
        else:
            return render_template("error.html", message="Reseptin poistaminen epäonnistui")
  
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            # session['csrf_token'] = secrets.token_hex(16)
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.username_in_database(username):
            return render_template("error.html", message="Käyttäjänimi on jo käytössä")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")