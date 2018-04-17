from flask import Flask
from flask_cas import CAS
from flask_cas import login_required
#from flask.ext.cas import CAS
#from flask.ext.cas import login_required
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

DEV = True


# Initialize the app
app = Flask(__name__)
# Initialize SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/cafapp_dev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Flask-Restful config
api = Api(app)
# CAS client config
cas = CAS(app)
app.config['CAS_SERVER'] = 'https://sso.gac.edu'
app.config['CAS_LOGIN_ROUTE'] = '/idp/profile/cas/login'
app.config['CAS_LOGOUT_ROUTE'] = '/idp/profile/cas/logout'
app.config['CAS_VALIDATE_ROUTE'] = '/idp/profile/cas/serviceValidate'
app.config['CAS_AFTER_LOGIN'] = 'default'

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 's3cr3t'

# Everything else is in the file CafApp.py
from app import CafApp
