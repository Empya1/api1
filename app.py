from flask import request, jsonify, Blueprint,session, Flask


import random

from flask_login import UserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pggf.sqlite3"
app.config["SECRET_KEY"] = "sddsfhxhdf"

db = SQLAlchemy(app)
admin = Admin(app)


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String())
	email = db.Column(db.String())
	password = db.Column(db.String())
	role = db.Column(db.String())
	pub_key = db.Column(db.String())
	pub = db.relationship("Pub", backref="users")
	comments = db.Relationship("Comment", backref="users")
	
	def __repr__(self):
		return f"< User: {self.name} >"
	
class Pub(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String())
	desc = db.Column(db.String())
	image = db.Column(db.String())
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
	url = db.Column(db.String())
	html_comp = db.relationship("HtmlComponent", backref="pub")
	
	def __repr__(self):
		return f"< Pub : {self.name} >"
	
class HtmlComponent(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	meta_title = db.Column(db.String())
	content = db.Column(db.String())
	pub_id = db.Column(db.Integer, db.ForeignKey("pub.id"))
	
	
	def __repr__(self):
		return f"< HtmlComponent : {self.name} >"
	
class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String())
	pub_id = db.Column(db.Integer, db.ForeignKey("pub.id"))
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
	
	def __repr__(self):
		
		return f"<Comment:{self.id}>"
		
with app.app_context():
	db.create_all()
	
	
admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Pub,db.session))
admin.add_view(ModelView(HtmlComponent,db.session))
#admin.add_view(ModelView,db.session)

#app = Blueprint("app", __name__, url_prefix="/app/")

#index
@app.route("/")

def index():
	
	for i in range(25):
		try:
			user = User(name=f"{i}",email=f"{i}",password=f"{i}",role=f"{i}",pub_key=f"{i}")
			
			db.session.add(user)
			db.session.commit()
			
		except:
			pass
		
	return jsonify({"app NAME": "ACCESS"})

#login
@app.route("/login", methods=["POST"])

def login():
	print("logging in")
	
	if request.is_json:
		
		try:
		
			data = request.json
			print("fetched data")
			
			user = User.query.filter(User.email==data["email"], User.pub_key==data["pub_key"]).all() 
			
			print(user)
			
			
			if len(user)==1:
				token = token_urlsafe(random.randint(20,40))
				print(token)
				return jsonify({"access_token":str(token)})
			
				
			else:
				print("not exist")
				return jsonify({"Error":"User does not exist or is not permitted"})
				
		except Exception as e:
			print(e)
			return jsonify({"Error":e})
			
	else: 
		print(e)
		return jsonify({"Error":"invalid request"})
		
		
@app.route("/pub/create")

def create_pub():
		
	data = request.json
		
	try:
			
		# FOR USER
		user_email = data["email"]
		user_password = data["password"]
			
		user = User.query.filter(User.email==user_email, User.password==user_password).first()
			
		#FOR PUB
			
		title = data["title"]
		desc = data["desc"]
		image = data["image"]
		user_id = user.id
		url = token_urlsafe(random.randint(8,20))
			
		#FOR HTML COMPONENT
		meta = data["meta"]
		content = data["content"]
		
			
		new_pub = Pub(title=title,desc=desc,image=image,user_id=user_id,url=url)
		db.session.add(new_pub)
		db.session.commit()
			
		pub_obj = Pub.query.filter(Pub.url==url, title==title).first()
			
		new_htmlcomponent = HtmlComponent(meta=meta,content=content,pub_id=pub_obj.id)
		db.session.add(new_htmlcomponent)
		db.session.commit()
			
	except Exception as e:
		return jsonify({"Error": e})
			
		
