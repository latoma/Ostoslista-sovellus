from flask import Flask
from os import getenv

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'a32ca29848ff340a5c28845c62f4af6b'
# FIX:
# app.secret_key = getenv("SECRET_KEY")

import routes