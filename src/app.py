from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Users(db.Model):
	__tablename__ = "users"
	id_user = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), nullable=False)
	email = db.Column(db.String(64), unique=True, nullable=False, index=True)
	password = db.Column(db.String(255), nullable=False)

	def __str__(self):
		return f"{self.name}"

@app.before_first_request
def create_database():
    db.create_all()

@app.route("/")
def index():
	users = Users.query.all()
	return render_template("users.html", users=users)

if __name__ == "__main__":
	app.run(debug=True)