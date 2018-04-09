from flask import Flask
from flask_cas import CAS
from flask_cas import login_required
#from flask.ext.cas import CAS
#from flask.ext.cas import login_required

# Initialize the app
app = Flask(__name__)

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
