from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app, prefix='/api/v1')

menus = {
    "Breakfast": {"menu":"price"},
    "Lunch": {"menu":"price"},
    "Dinner":{"menu":"price"}
}

parser = reqparse.RequestParser()

class ViewMenu(Resource):
    def get(self):
        return menu

class AddMenuItems(Resource):
     def post(self):
        args = parser.parse_args()
        menu_id = int(max(menus.keys()).lstrip('meal'))+1
        menu_id = 'menu%i' % menu_id
        menus[menu_id] = {'menu':args['price']}
        return menus[menu_id], 201

api.add_resource(ViewMenu, '/menu')
api.add_resource(AddMenuItems, '/addMenuItem')

if __name__ == '__main__':
    app.run(debug=True)