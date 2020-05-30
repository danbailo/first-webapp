from datetime import datetime, timedelta

from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models import User


def init_app(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/users")
    def users():
        users_result = User.query.all()
        return render_template("users.html", users=users_result)

    @app.route("/users/<int:id_user>")
    @login_required
    def user(id_user):
        user = User.query.get(id_user)
        return render_template("user.html", user=user)

    @app.route("/users/delete/<int:id_user>")
    def delete(id_user):
        user = User.query.filter_by(id_user=id_user).first()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('users'))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            user = User()
            user.name = request.form.get("name")
            user.email = request.form.get("email")
            user.password =\
                generate_password_hash(request.form.get("password"))
            user.date_create = datetime.now()
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('users'))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email")
            user = User.query.filter_by(email=email).first()
            if not user:
                flash("User not found!", "danger")
                return redirect("")

            password = request.form.get("password")
            if not check_password_hash(user.password, password):
                flash("Password incorrect!", "warning")
                return redirect("")

            remember = request.form.get("remember")

            login_user(user, remember=remember, duration=timedelta(days=7))
            flash("Login successfully!", "success")
            return redirect(url_for('users'))

        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('users'))
