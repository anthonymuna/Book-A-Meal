from flask import Flask, request, jsonify, make_response
import jwt, datetime
from models import db, User
# from functools import wraps

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'this is the secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/ApiAuthdb'
heroku = Heroku(app)
db.init_app(app)

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):


@app.route('/api/v1/auth/view/user', methods=['GET'])
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

@app.route('/api/v1/auth/user/<user_id>', methods=['GET'])
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

@app.route('/api/v1/auth/create/user', methods=['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], data['confirmPassword'], method=sha256)

    new_user = User(name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"New User Successfully Created"})

@app.route('/api/v1/auth/update/user', methods=['PUT'])
def update_user():
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({'message':'No user found'})

    user.admin = True
    db.session.commit()
    return jsonify({"message": "The user current priviledges have been upgraded"})

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user():
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