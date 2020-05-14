from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = "login"
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String,nullable=False)
	password = db.Column(db.String,nullable=False)

class Topics(db.Model):
	__tablename__="topics"
	id = db.Column(db.Integer,autoincrement=True,nullable=False)
	name = db.Column(db.String,primary_key=True)
	desc = db.Column(db.String,nullable=False)
	imgurl = db.Column(db.String,nullable=False)
	table = db.Column(db.String)
	
class Elements(db.Model):
	__tablename__="elements"
	atomic_number = db.Column(db.Integer,nullable=False,primary_key=True)
	atomic_mass = db.Column(db.Float,nullable=False)
	density = db.Column(db.Float,nullable=False)
	color = db.Column(db.String)
	inventor = db.Column(db.String)
	state_at_20 = db.Column(db.String)
	group =db.Column(db.Integer)
	period =db.Column(db.Integer)
	melting_point =db.Column(db.Float)
	boiling_point = db.Column(db.Float)
	electronic_config = db.Column(db.String)
	block = db.Column(db.String)
	uses = db.Column(db.String)
	name = db.Column(db.String)
class Electronic(db.Model):
	__tablename__="electronic"
	atomic_number = db.Column(db.Integer,nullable=False,primary_key=True)
	name = db.Column(db.String,nullable=False)
	uses = db.Column(db.String)
	inventor = db.Column(db.String)
	img_url = db.Column(db.String,nullable=False) 	