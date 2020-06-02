from flask import flash, redirect, render_template, url_for
from flask_login import current_user

from app import db
from app.forms import BookForm, UserBookForm
from app.models import Book

from . import book

@book.route("/book/add", methods=["GET", "POST"])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book()
        book.book = form.name.data
        db.session.add(book)
        db.session.commit()
        flash("Book create with successfully!", "success")
        return redirect(url_for(".add_book"))
    return render_template("book/add.html", form=form)

@book.route("/user/<int:id>/add_book", methods=["GET", "POST"])
def add_book_user(id):
    form = UserBookForm()

    if form.validate_on_submit():
        book = Book.query.get(form.book.data)
        current_user.books.append(book)
        db.session.add(current_user)
        db.session.commit()
        flash("Book create with successfully!", "success")
        return redirect(url_for(".add_book_user", id=current_user.id_user))            

    return render_template("book/add_book.html", form=form)
