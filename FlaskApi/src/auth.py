from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app, prefix='/api/v1/auth')


signup = {
    "users1": {"name":"Anthony Muna","email":"anthony@gmail.com", "password":"12345"},
    "users2": {"name":"Carol Kamau", "email":"carol@gmail.com", "password":"54321"},
}

login = {
    "user1": {"name": "Anthony Muna", "email":"anthony@gmail.com"},
    "user2": {"name":"Carol Kamau", "email":"carol@gmail.com"},
}

parser = reqparse.RequestParser()
parser.add_argument('register_user')

class signin(Resource):
    def get(self):
        return login
    
class RegisterUsers(Resource):
    def post(self):
        args = parser.parse_args()
        users = int(max(signup.keys()).lstrip('user'))+1
        users = 'user%i' % users
        signup[users] = {'name':args['email']}
        return signup[users], 201

    def get(self):
        return{"user":signup}

api.add_resource(signin, '/login')
api.add_resource(RegisterUsers, '/signup')

if __name__ == '__main__':
    app.run(debug=True)
