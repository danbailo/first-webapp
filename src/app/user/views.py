from flask import redirect, render_template, url_for
from flask_login import login_required

from app import db
from app.models import User

from . import user


@user.route("/")
@user.route("/users")
def users():
    users_result = User.query.all()
    return render_template("users.html", users=users_result)


@user.route("/users/<int:id_user>")
@login_required
def user_info(id_user):
    user = User.query.get(id_user)
    return render_template("user.html", user=user)


@user.route("/users/delete/<int:id_user>")
def delete(id_user):
    user = User.query.filter_by(id_user=id_user).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('.users'))
