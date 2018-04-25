from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'this is the secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = ''

db.SQLAlchemy(app)

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

	 user
	return ''

@app.route('/user/<user_id>', methods=['DELETE'])
if __name__ == '__main__':
	app.run(debug=True)