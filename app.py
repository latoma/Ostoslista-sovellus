from flask import Flask
from os import getenv
import routes

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")