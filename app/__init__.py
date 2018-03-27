from flask import Flask

# Initialize the app
app = Flask(__name__)

# Everything else is in the file CafApp.py
from app import CafApp

# This chunk of code will enable logging to the file tmp/cafapp.log
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/cafapp.log', 'a', 1*1024*1024,10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('CafApp just started!')
