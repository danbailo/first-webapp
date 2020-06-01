from datetime import datetime, timedelta

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models import User, Book
from app.forms import LoginForm, RegisterForm, BookForm, UserBookForm

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
        form = RegisterForm()
        if form.validate_on_submit():
            user = User()
            user.name = form.name.data
            user.email = form.email.data
            user.password = generate_password_hash(form.password.data)
            user.date_create = datetime.now()
            db.session.add(user)
            db.session.commit()
            flash("User create with successfully!", "success")
            return redirect("")

        return render_template("register.html", form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if not user:
                flash("User not found!", "danger")
                return redirect("")

            if not check_password_hash(user.password, form.password.data):
                flash("Password incorrect!", "warning")
                return redirect("")

            login_user(user, remember=form.remember.data,
                       duration=timedelta(days=7))

            flash("Login successfully!", "success")
            return redirect(url_for('users'))

        return render_template("login.html", form=form)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('users'))

    @app.route("/book/add", methods=["GET", "POST"])
    def add_book():
        form = BookForm()
        if form.validate_on_submit():
            book = Book()
            book.book = form.name.data
            db.session.add(book)
            db.session.commit()
            flash("Book create with successfully!", "success")
            return redirect("")
        return render_template("book/add.html", form=form)

    @app.route("/user/<int:id>/add_book", methods=["GET", "POST"])
    def add_book_user(id):
        form = UserBookForm()
        return render_template("book/add_book.html", form=form)