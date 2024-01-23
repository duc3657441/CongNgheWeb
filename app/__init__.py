from flask import Flask
from app.connect import connect
from flask_session import Session
# from datetime import timedelta
app = Flask(__name__)

app.config["SECRET_KEY"] = "test"

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_AGE"] = 1800
Session(app)

from app import routes