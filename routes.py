from app import app
from flask import render_template, request, redirect, flash
import users, shopping_lists, recipes
from datetime import datetime

@app.route("/")
def index():
    if users.user_id() == 0:
        return render_template("index.html")
    else:
        return render_template("index.html", 
                               lists = shopping_lists.get_shopping_lists(), 
                               recipe_list = recipes.get_recipes())

@app.route("/list")
def list():
    shared = shopping_lists.get_shared_users()
    if shared:
        return render_template("list.html", 
                               list_name = shopping_lists.get_list_name(), 
                               shared_to = shared, 
                               items = shopping_lists.get_items(), 
                               recipe_list = recipes.get_recipes())
    else:
        return render_template("list.html", 
                               list_name = shopping_lists.get_list_name(), 
                               items = shopping_lists.get_items(), 
                               recipe_list = recipes.get_recipes())
    
@app.route("/recipe")
def recipe():
    return render_template("recipe.html", 
                           recipe_name = recipes.get_recipe_name(), 
                           items = recipes.get_recipe_items())

@app.route("/activate_list", methods=['POST'])
def activate_list():
    if request.method == "POST":
        list_id = request.form["list_id"]
        shopping_lists.set_active_list_id(list_id)
        return redirect("/list")
    
@app.route("/share_list", methods=["GET", "POST"])
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
            message = f"Käyttäjää {username} ei löytynyt"

        else: 
            state = shopping_lists.share_list(username)
            if state:
                message = f"Jakaminen käyttäjälle {username} onnistui"
            else:
                message = "SQL virhe"
            
        return render_template("share.html", 
                               success = state,
                               message = message)
        

@app.route("/activate_recipe", methods=['POST'])
def activate_recipe():
    if request.method == 'POST':
        recipe_id = request.form["recipe_id"]
        recipes.set_session_recipe_id(recipe_id)
        return redirect("/recipe")
    

@app.route("/delete_list", methods=["POST"])
def delete_list():
    if request.method == "POST":
        shopping_lists.delete_list()
    return redirect("/")

@app.route("/delete_recipe", methods=["POST"])
def delete_recipe():
    if request.method == "POST":
        recipes.delete_recipe()

    return redirect("/")

# Renders  a template either for a new shopping_list or a new recipe
@app.route("/new_list", methods=['GET', 'POST'])
def new_list():
    if request.method == "GET":
        return render_template("new_list.html", current_date = datetime.now().strftime('%d/%m/%Y'))

    if request.method == "POST":
        if shopping_lists.new(request.form["list_name"]):
            return redirect("/list")
            
        
@app.route("/new_recipe", methods=['GET', 'POST'])
def new_recipe():
    if request.method == "GET":
        return render_template("new_recipe.html")

    if request.method == "POST":
        if recipes.new(request.form["recipe_name"]):
            return redirect("/recipe")
        else:
            return render_template("error.html", message="Reseptin alustaminen ei onnistunut")
            

@app.route("/add_list_item", methods=["POST"])
def add_item():
    if request.method == "POST":
        item_desc = request.form["content"]
        if shopping_lists.add_item(item_desc):
            return redirect("/list")
        else:
            return  render_template("error.html", message="Tuotteen lisääminen ei onnistunut")
            
        
@app.route("/add_recipe_item", methods=["POST"])
def add_recipe_item():
    if request.method == "POST":
        item_desc = request.form["content"]
        if recipes.add_item(item_desc):
                return redirect("/recipe")
        else:
            return render_template("error.html", message="Tuotteen lisääminen ei onnistunut")


@app.route("/remove_list_items", methods=["POST"])
def remove_list_items():
    if request.method == "POST":
        removed_item_ids_string = request.form.get('removedItems')
        if removed_item_ids_string is not None and removed_item_ids_string != "":
            removed_item_ids = [int(x) for x in removed_item_ids_string.split(",")]
            shopping_lists.remove_items(removed_item_ids)

        return redirect("/list")
    
@app.route("/remove_recipe_items", methods=["POST"])
def remove_recipe_items():
    if request.method == "POST":
        removed_item_ids_string = request.form.get('removedItems')
        if removed_item_ids_string is not None and removed_item_ids_string != "":
            removed_item_ids = [int(x) for x in removed_item_ids_string.split(",")]
            recipes.remove_items(removed_item_ids)

        return redirect("/recipe")        

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
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
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")