from app import app
from flask import render_template, request, redirect
import users, shopping_lists

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/list")
def list():
    return render_template("list.html", items = shopping_lists.get_items())

@app.route("/new", methods=['POST'])
def new():
    shopping_lists.new()
    return redirect("/list")

@app.route("/add_item", methods=["POST"])
def add_item():
    content = request.form["content"]
    if shopping_lists.add_item(content):
        return render_template("list.html", items = shopping_lists.get_items())
    else:
        return  render_template("error.html", message="Tuotteen lisääminen ei onnistunut")
    
@app.route("/removal_mode", methods=["POST"])
def removal_mode():
    return render_template("remove.html", items = shopping_lists.get_items())

@app.route("/confirm_removals", methods=["POST"])
def confirm_removals():
    # Puts the ids of removed items into a list and calls remove_items()
    removed_item_ids_string = request.form.get('removedItems')
    if removed_item_ids_string != "":
        removed_item_ids = [int(x) for x in removed_item_ids_string.split(",")]
        shopping_lists.remove_items(removed_item_ids)

    return render_template("list.html", items = shopping_lists.get_items())

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
        
@app.route("/home")
def home():
    return redirect("/")