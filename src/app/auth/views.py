from datetime import datetime, timedelta

from flask import flash, redirect, render_template, url_for
from flask.globals import request
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.forms import LoginForm, RegisterForm
from app.models import User
# from app.user.views import confirm

from . import auth


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        email = form.email.data
        if user.query.filter_by(email=email).first():
            flash("This email already in use!", "danger")
            return redirect(url_for(".register"))
        user.name = form.name.data
        user.email = form.email.data
        user.password = generate_password_hash(form.password.data)
        user.date_create = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash("User create with successfully!", "success")
        link = request.url_root[:-1] + url_for('user.confirm',
                                               id_user=user.id_user)
        print(f"click here to active you account {link}")
        return redirect(url_for(".register"))

    return render_template("register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash("User not found!", "danger")
            return redirect(url_for(".login"))

        if not user.confirmed:
            flash("User not confirmed!", "warning")
            return redirect(url_for(".login"))

        if not check_password_hash(user.password, form.password.data):
            flash("Password incorrect!", "warning")
            return redirect(url_for(".login"))

        login_user(user, remember=form.remember.data,
                   duration=timedelta(days=7))

        flash("Login successfully!", "success")
        return redirect(url_for('user.users'))

    return render_template("login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.users'))
