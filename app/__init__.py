from flask import Flask
from app.connect import connect
app = Flask(__name__)
from app import routes