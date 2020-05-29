from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
	__tablename__ = "users"
	id_user = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), nullable=False)
	email = db.Column(db.String(64), unique=True, nullable=False, index=True)
	password = db.Column(db.String(255), nullable=False)

	def __str__(self):
		return f"{self.name}"

@app.route("/")
def index():
	users = User.query.all()
	return render_template("users.html", users=users)

@app.route("/users/delete/<int:id_user>")
def delete(id_user):
	user = User.query.filter_by(id_user=id_user).first()
	db.session.delete(user)
	db.session.commit()
	return redirect(url_for('index'))

if __name__ == "__main__":
	db.create_all()
	app.run(debug=True)