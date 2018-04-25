from api import db

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
	description = db.Column(String(250))
    price = db.Column(db.String(8))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    restaurant = db.relationship('Restaurant', backref='name', lazy=True)