from app import app
from flask import render_template, request, redirect
import users, shopping_lists
from datetime import datetime

@app.route("/")
def index():
    if users.user_id() == 0:
        return render_template("index.html")
    else:
        return render_template("index.html", lists = shopping_lists.get_shopping_lists())

@app.route("/list")
def list():
    return render_template("list.html", list_name = shopping_lists.get_list_name(), items = shopping_lists.get_items())

@app.route("/activate_list", methods=['GET', 'POST'])
def activate_list():
    if request.method == "POST":
        list_id = request.form["list_id"]
        shopping_lists.set_active_list_id(list_id)
    return list()

@app.route("/delete_list", methods=["POST"])
def delete_list():
    if request.method == "POST":
        shopping_lists.delete_list()
    return index()


@app.route("/new", methods=['GET', 'POST'])
def new():
    if request.method == "GET":
        return render_template("new.html", current_date = datetime.now().strftime('%d/%m/%Y'))
    
    if request.method == "POST":
        if shopping_lists.new(request.form["list_name"]):
            return list()
        else:
            return  render_template("error.html", message="Tuotteen lisääminen ei onnistunut")

@app.route("/add_item", methods=["POST"])
def add_item():
    if request.method == "POST":
        content = request.form["content"]
        if shopping_lists.add_item(content):
            return list()
        else:
            return  render_template("error.html", message="Tuotteen lisääminen ei onnistunut")

    
@app.route("/remove_items", methods=["POST"])
def remove_items():
    # Removes selected items from shopping list
    if request.method == "POST":
        removed_item_ids_string = request.form.get('removedItems')
        if removed_item_ids_string is not None and removed_item_ids_string != "":
            # Goes through list of selected item_ids and removes them
            removed_item_ids = [int(x) for x in removed_item_ids_string.split(",")]
            shopping_lists.remove_items(removed_item_ids)

        return list()


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