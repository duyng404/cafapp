from flask import render_template, jsonify
from app import api, app, cas
from flask_cas import login_required
from app.api.order import *
import app.api.order as order
from app.api.user import UserApi, UsersApi


api.add_resource(OrderApi,       '/api/v1/orders/<int:order_id>')
api.add_resource(OrderStatusApi, '/api/v1/orders/<int:order_id>/status')
api.add_resource(OrdersApi,      '/api/v1/orders')
api.add_resource(UserApi,        '/api/v1/users/<string:username>')
api.add_resource(UsersApi,       '/api/v1/users')

@app.route('/api/v1/prep/<int:run_flag>', methods=['GET'])
def start_or_stop(run_flag):
    if run_flag:
        PrepQueueApi.turn_on()
    else:
        PrepQueueApi.turn_off()

@app.route('/api/v1/orders/active', methods=['GET'])
def get_all_orders():
    return jsonify(order._active_orders.serialize)

@app.route('/')
@login_required
def default():
    print('someone access this page')
    print('dir=',dir(cas))
    print('vars:')
    attrs = vars(cas)
    print(', '.join("%s: %s" % item for item in attrs.items()))
    return render_template('index.html', username=cas.username)
