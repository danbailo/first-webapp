from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def current_user(id_user):
	return User.query.get(id_user)

class User(db.Model):
	__tablename__ = "users"
	id_user = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), nullable=False)
	email = db.Column(db.String(64), unique=True, nullable=False, index=True)
	password = db.Column(db.String(255), nullable=False)
	profile = db.relationship('Profile', backref='user', uselist=False)

	def __str__(self):
		return f"{self.name}"

class Profile(db.Model):
	__tablename__ = "profiles"
	id_profile = db.Column(db.Integer, primary_key=True)
	photo = db.Column(db.Unicode(124), nullable=False)
	id_user = db.Column(db.Integer, db.ForeignKey("users.id_user"))

	def __str__(self):
		return f"{self.name}"


@app.route("/")
def index():
	users = User.query.all()
	return render_template("users.html", users=users)

@app.route("/users/<int:id_user>")
def unique(id_user):
	user = User.query.get(id_user)
	return render_template("user.html", user=user)

@app.route("/users/delete/<int:id_user>")
def delete(id_user):
	user = User.query.filter_by(id_user=id_user).first()
	db.session.delete(user)
	db.session.commit()
	return redirect(url_for('index'))

@app.route("/register")
def register():
	return render_template("register.html")

@app.route("/login")
def login():
	return render_template("login.html")	

if __name__ == "__main__":
	db.create_all()
	app.run(debug=True)