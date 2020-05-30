from app import db, login_manager
from flask_login import UserMixin


class Profile(db.Model):
    __tablename__ = "profiles"
    id_profile = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.Unicode(124), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey("users.id_user"))

    def __str__(self):
        return f"{self.name}"


@login_manager.user_loader
def current_user(id_user):
    return User.query.get(id_user)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    date_create = db.Column(db.DateTime, nullable=False)
    profile = db.relationship('Profile', backref='user', uselist=False)

    def get_id(self):
        return self.id_user

    def __str__(self):
        return f"{self.name}"
