from app import cas, db, DEV
from app.data.orders import Order, Menu
from app.data.user import User
from app.api.permissions import is_admin, valid_call
from flask_restful import abort, Resource, reqparse

from collections import deque
from datetime import datetime
import threading
import time


_WAIT_QUEUE = deque()


class _Worker(threading.Thread):
    _CAPACITY = 10
    _RELOAD_TIME = 15  # In minutes
    '''
    Automatically moves things from the Wait Queue to the Prep Queue
    '''
    def __init__(self, queue):
        super(_Worker, self).__init__()
        self._queue = queue
        self._stop_event = threading.Event()
        self._stopped = True

    def run(self):
        self._stopped = False
        while True:
            time.sleep(self._RELOAD_TIME * 60)
            if self.stopped:
                break
            with self._queue.lock:
                for _ in range(10):
                    self._queue.add(_WAIT_QUEUE.pop(), 2)

    def stop(self):
        self._stop_event.set()
        self._stopped = True

    @property
    def stopped(self):
        return self._stop_event.is_set() or self._stopped

class OrderTracker:
    lock = threading.Lock()
    def __init__(self):
        self.d = {}
        self._thread = _Worker(self)

    def __getattr__(self, item):
        return self.d[item]

    def add(self, key, value):
        self.d[key] = value

    @property
    def serialize(self):
        with self.lock:
            prep = []
            heating = []
            delivery = []
            for key, value in self.d.items():
                if value == 1:
                    prep.append(key)
                elif value == 2:
                    heating.append(key)
                else:
                    delivery.append(key)


            return {
                'prep'    : [item.serialize for item in Order.query.filter(Order.id.in_(prep))],
                'heating' : [item.serialize for item in Order.query.filter(Order.id.in_(heating))],
                'delivery': [item.serialize for item in Order.query.filter(Order.id.in_(delivery))]
            }

_active_orders = OrderTracker()


class PrepQueueApi(Resource):
    method_decorators = [is_admin]

    @staticmethod
    def turn_on():
        _active_orders._thread.run()

    @staticmethod
    def turn_off():
        _active_orders._thread.stop()


    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('time', type=int)
        parser.add_argument('orders', type=int)

        args = parser.parse_args()
        _Worker._RELOAD_TIME = args.get('time', _Worker._RELOAD_TIME)
        _Worker._CAPACITY = args.get('orders', _Worker._CAPACITY)

        return None, 204

class OrderApi(Resource):
    method_decorators = [valid_call]

    def get(self, order_id):
        return Order.query.filter(Order.id == order_id).one().serialize

    def put(self, order_id):
        pass


class OrdersApi(Resource):
    method_decorators = [valid_call]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('owner', required=True)
        parser.add_argument('content', action='append', required=True)
        args = parser.parse_args()
        args['created'] = datetime.now()
        args['status'] = 1
        if DEV:
            owner = User.query.filter(User.username == args['owner']).one()
        else:
            owner = User.query.filter(User.username == cas.username).one()
        contents = [Menu.query.filter_by(id=item).one() for item in args['content']]
        del args['content']
        order = Order(**args)
        db.session.add(order)
        owner.orders.append(order)
        order.contents.extend(contents)
        db.session.commit()
        _WAIT_QUEUE.appendleft(order.id)
        return order.serialize, 201

class OrderStatusApi(Resource):
    '''
    0 is wait queue
    1 is prep queue
    2 is hot lamp
    3 is delivery
    4 is done
    '''
    method_decorators = [is_admin]

    def get(self, order_id):
        return _active_orders[order_id]

    def put(self, order_id):
        parser = reqparse.RequestParser()
        parser.add_argument('from', type=int, required=True)
        parser.add_argument('to', type=int, required=True)

        args = parser.parse_args()
        if args['from'] in (0, 4):
            abort(404)

        if args['from'] != _active_orders[order_id]:
            abort(404)

        _active_orders[order_id] = args['to']
        o = Order.query.get(order_id)
        o.status = args['to']

        return None, 204
