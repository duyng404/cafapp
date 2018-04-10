from app.data.orders import Order
from app.api.permissions import valid_call
from flask_restful import Resource, reqparse

class OrderApi(Resource):
    @valid_call
    def get(self, order_id):
        return Order.query.filter_by(Order.id == order_id).one().serialize

    @valid_call
    def put(self, order_id):
        pass
