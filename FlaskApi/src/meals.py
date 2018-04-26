from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app, prefix='/api/v1')

meals = {
    "Breakfast": {
        "meal":"Tea with mahamri", "price":"150","meal":"Porridge", "price":"80", "meal":"English Breakfast", "meal":"Arrow root", 
        "price":"50", "meal":"Sweet potato", "price": "60"},
    "Lunch": {
        "meal":"Ugali and Stew", "price":"200", "meal":"Mashed peas and potato mix",
        "meal": "Githeri", "price": "100", 
        "meal":"Kenyan Pilau", "price": "110",
        "meal":"Kenyan Stew", "price":"80"
    },
    "Dinner":{
        "meal":"Nyama Choma", "price":"200", "meal":"Beef",
        "price": "200", "meal":"matoke", "price":"200",
        "meal": "Chapati and stew", "price":"150",
        "meal":"coconut rice", "price":"100"
    }
}

parser = reqparse.RequestParser()

class ListMeals(Resource):
    def get(self):
        return meals
    
    def put(self, meal_id):
        args = parser.parse_args()
        meal = {'meal': args['meal']}
        meals[meal_id] = meal
        return meal, 201

    def delete(self, meal_id):
        del meals[meal_id]
        return "Meal deleted", 204

class AddMeals(Resource):
     def post(self):
        args = parser.parse_args()
        meal_id = int(max(meals.keys()).lstrip('meal'))+1
        meal_id = 'meal%i' % meal_id
        meals[meal_id] = {'meal':args['price']}
        return meals[meal_id], 201

api.add_resource(ListMeals, '/meals')
api.add_resource(AddMeals, '/add')

if __name__ == '__main__':
    app.run(debug=True)