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
	return "<a href='/posts'>Posts</a>"

@app.route("/response")	
def get_response():
	return render_template("response.html")

@app.route("/redirect")
def _redirect():
	return redirect(url_for("get_response")) #name of function, status code 302

@app.route("/posts")
@app.route("/posts/<int:id_>")
def posts(id_=None):
	title = request.args.get("title")
	data = {
		"path": request.path,
		"referrer": request.referrer,
		"content_type": request.content_type,
		"method": request.method,
		"title": title,
		"id_": id_
	}
	print(data)
	return data	

if __name__ == "__main__":
	app.run(debug=True)