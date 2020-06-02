from datetime import datetime, timedelta

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models import User, Book
from app.forms import LoginForm, RegisterForm, BookForm, UserBookForm

from app.auth import auth as auth_blueprint

def init_app(app):
    app.register_blueprint(auth_blueprint)

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

        if form.validate_on_submit():
            book = Book.query.get(form.book.data)
            current_user.books.append(book)
            db.session.add(current_user)
            db.session.commit()
            flash("Book create with successfully!", "success")
            return redirect(url_for("add_book_user", id=current_user.id_user))            

        return render_template("book/add_book.html", form=form)