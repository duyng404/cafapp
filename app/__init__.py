from flask import Flask

# Initialize the app
app = Flask(__name__)
app.config['DEBUG'] = True

# Everything else is in the file CafApp.py
from app import CafApp
