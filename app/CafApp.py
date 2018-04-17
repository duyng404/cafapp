from flask import render_template
from app import api, app, cas, DEV
from flask_cas import login_required
from app.api.order import OrderApi
from app.api.user import UserApi, UsersApi
from app.api.permissions import our_login_required


api.add_resource(OrderApi, '/api/v1/orders/<int:order_id>')
api.add_resource(UserApi, '/api/v1/users/<string:username>')
api.add_resource(UsersApi, '/api/v1/users')

@app.route('/')
@our_login_required
def landing_UI():
    if not DEV:
        return render_template('index.html', username=cas.username)
    else:
        username = 'dev_mode'
        return render_template('index.html', username=username)

