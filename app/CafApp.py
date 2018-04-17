from flask import render_template
from app import api, app, cas
from flask_cas import login_required
from app.api.order import OrderApi, OrdersApi
from app.api.user import UserApi, UsersApi


api.add_resource(OrderApi,  '/api/v1/orders/<int:order_id>')
api.add_resource(OrdersApi, '/api/v1/orders/')
api.add_resource(UserApi,   '/api/v1/users/<string:username>')
api.add_resource(UsersApi,  '/api/v1/users')



@app.route('/')
@login_required
def default():
    print('someone access this page')
    print('dir=',dir(cas))
    print('vars:')
    attrs = vars(cas)
    print(', '.join("%s: %s" % item for item in attrs.items()))
    return render_template('index.html', username=cas.username)
