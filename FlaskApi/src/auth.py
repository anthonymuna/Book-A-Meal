from flask import Flask, request, jsonify, make_response
import jwt, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'this is the secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://sbzixdifvzzerw:6cf6a7983d3097cfe0b7be50f54d5a9d76c499258a9367c76bc4b41757bb49a2@ec2-107-20-151-189.compute-1.amazonaws.com:5432/damgk29n0lgnoh'

db = SQLAlchemy(app)

#Models start
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(200))
    description = db.Column(db.String(250))
    price = db.Column(db.String(8))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    restaurant = db.relationship('Restaurant', backref='restaurantName', lazy=True)
#models end

@app.route('/api/auth/view/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['name'] = user.name
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['admin'] = user.admin
        output.append(user_data)
    return jsonify({'users':output})

@app.route('/api/auth/view/user/<user_id>', methods=['GET'])
def get_one_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({'message':'No user found'})

    user_data = {}
    user_data['name'] = user.name
    user_data['username'] = user.username
    user_data['email'] = user.email
    user_data['admin'] = user.admin

    return jsonify({'user':user_data})

@app.route('/api/auth/create', methods=['GET','POST'])
def create_user(user_id):
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], data['confirmPassword'])
    new_user = User(name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"New User Successfully Created"})

@app.route('/api/auth/update', methods=['PUT'])
def update_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({'message':'No user found'})

    user.admin = True
    db.session.commit()
    return jsonify({"message": "The user current priviledges have been upgraded"})

@app.route('/api/auth/delete/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({'message':'No user found'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "The user has been deleted"})

@app.route('/api/auth/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response("Could not verify", 401,{'Authentication': 'Basic Response="Login required"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response("Could not verify", 401,{'Authentication': 'Basic Response="Login required"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id':user.user_id, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    make_response("Could not verify", 401,{'Authentication': 'Basic Response="Login required"'})


if __name__ == '__main__':
    app.run(debug=True)