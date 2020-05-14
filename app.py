#importing all the required libraries
from flask import Flask, session,request,render_template,redirect,flash,url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from werkzeug.security import check_password_hash, generate_password_hash
import requests
from models import *
import time
from werkzeug.utils import secure_filename#for file uploading
#####################################
import sys
import wikipediaapi
from prediction import *
wiki_wiki = wikipediaapi.Wikipedia('en')
def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)
UPLOAD_FOLDER = os.path.join(os.path.join(os.getcwd(),'static'),'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Tell Flask what SQLAlchemy databas to use.
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Link the Flask app with the database (no Flask app is actually being run yet).
db.init_app(app)

#various routes for the website
#login part
@app.route("/",methods=["GET","POST"])
def login():
	if session.get("user") is None:
		if request.method == "GET":
			return render_template('index.html',info=['login','UserName','Password','register'])
		else:
			name = request.form.get("name")
			password =request.form.get("password")
			user = User.query.filter_by(name=name).first()
			time.sleep(0.5);
			if user is None:
				flash('No user found with that sort of name')
				return redirect("/")
			elif not check_password_hash(user.password,password):
				flash("you password is incorrect")
				return redirect("/")
			else:
				session["user"]=user.name
				return redirect('/home')
	else:
		return redirect('/home')
#register part				
@app.route("/register",methods=["GET","POST"])
def register():
	if session.get("user") is None:
		if request.method == "GET":
			return render_template('index.html',info=['register','Your UserName','Your Password','login'])
		elif request.method == "POST":
			name = request.form.get("name")
			password =request.form.get("password")
			password_hash = generate_password_hash(password)
			user = User.query.filter_by(name=name).first()
			if user is None: 
				user = User(name=name,password=password_hash)
				session["user"]=user.name	
				db.session.add(user)
				db.session.commit()
				return redirect('/home')
			else:
				flash('User Name is Taken')
				return redirect('/register')	
	else:
		return redirect('/home')			
@app.route("/home")
def home():
	if session.get("user") is None:
		return redirect('/')
	data = Topics.query.all()
	return render_template('home2.html',data=data,nav=['logout','contact','about','search'],user=session.get("user"),)
@app.route("/logout")
def logout():
	session.clear()
	return redirect("/")	
@app.route("/home/<string:val>",methods=["GET","POST"])
def main(val):
	if request.method =="GET":
		if session.get("user") is None:
			return redirect('/')	
		if val!="Image":
			elements = str_to_class(val).query.all()
			return render_template('main.html',elements=elements,table=val,user=session.get("user"))	
		else:
			return redirect('/upload')	
	else:
		if session.get("user") is None:
			return redirect('/')
		asked = request.form.get(val);	
		print(asked.isdigit())	
		if val!="Image":
			if not asked.isdigit():
				elements = str_to_class(val).query.filter(str_to_class(val).name.ilike("%"+asked+"%")).all()		
			else:
				elements = str_to_class(val).query.filter(str_to_class(val).atomic_number==asked).all()
			return render_template('main.html',elements=elements,table=val,user=session.get('user'))	
		else:
			flash('some internal error!!')
			return redirect('/home')		
@app.route("/home/<string:val>/<string:name>",methods=["GET"])
def model(val,name):
	if request.method =="GET":
		if session.get("user") is None:
			return redirect('/')
		if val!="Image":
			element = str_to_class(val).query.filter(str_to_class(val).name==name).first()
			if element is not None:
				element = element.__dict__
				page_py = wiki_wiki.page(element["name"])
				element.pop('_sa_instance_state')
				summary="" 
				if page_py.exists():
					summary=page_py.summary
				return render_template('element.html',element=element,table=val,summary=summary,user=session.get("user"))
			else:
				flash("Retry Once again or element not in our database")
				return redirect('/home')	
		else:
			return redirect('/home')

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash("No file part recieved")
            return redirect('/upload')
        file = request.files['file']
        print(allowed_file(file.filename))
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash("No file selcted")
            return redirect('/upload')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path_of_file =os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path_of_file)
            predicted = predict(path_of_file)
            flash("our model predicted "+predicted)
            os.remove(path_of_file)
            return redirect(url_for('model',val='Electronic',name=predicted))
        else:
        	flash("file format not supported")
        	return redirect('/upload')	      
    elif request.method == 'GET':
    	if session.get('user') is None:
    		return redirect('/')
    	return render_template('upload.html',user=session.get('user'))                                          





            

