from app import cas, db, DEV
from app.data.orders import Order
from app.data.user import User
from app.api.permissions import is_admin, valid_call
from flask_restful import Resource, reqparse

from collections import deque
from datetime import datetime
import threading
import time

WAIT_QUEUE = deque()

class PrepQueue:
    CAPACITY = 10
    RELOAD_TIME = 15 # In minutes
    lock = threading.Lock()
    def __init__(self):
        self.l = []

    class Worker(threading.Thread):
        def __init__(self):
            super(PrepQueue.Worker, self).__init__()
            self._stop_event = threading.Event()

        def run(self):
            while True:
                time.sleep(PrepQueue.RELOAD_TIME * 60)
                if self.stopped:
                    break
                with PrepQueue.lock:
                    for _ in range(10):
                        pass


        def stop(self):
            self._stop_event.set()

        @property
        def stopped(self):
            return self._stop_event.is_set()




class OrderApi(Resource):
    @valid_call
    def get(self, order_id):
        return Order.query.filter_by(Order.id == order_id).one().serialize

    @is_admin
    def put(self, order_id):
        pass


class OrdersApi(Resource):
    method_decorators = [valid_call]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('owner')
        parser.add_argument('content', action='append')
        args = parser.parse_args()
        args['created'] = datetime.now()
        if DEV:
            owner = User.query.filter_by(User.username == args['owner']).one()
        else:
            owner = User.query.filter_by(User.username == cas.username)


        order = Order(**args)
        owner.orders.append(order)
        db.session.add(order)
        db.session.save()
        WAIT_QUEUE.appendleft(order.id)
        return order.serialize, 201
