from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app, prefix='/api/v1')

orders = {
    "day": {"order": "date"},
    "history": {"order": "date"}
}

parser = reqparse.RequestParser()

class ListUpdateOrders(Resource):
    def get(self):
        return orders
    
    def put(self, order_id):
        args = parser.parse_args()
        order = {'order': args['date']}
        orders[order_id] = order
        return order_id, 201

class AddOrders(Resource):
     def post(self):
        args = parser.parse_args()
        order_id = int(max(orders.keys()).lstrip('order'))+1
        order_id = 'order%i' % order_id
        orders[order_id] = {'order':args['date']}
        return orders[order_id], 201

api.add_resource(ListUpdateOrders, '/admin/orders')
api.add_resource(AddOrders, '/admin/orders/add')

if __name__ == '__main__':
    app.run(debug=True)