from app import db, login_manager
from flask_login import UserMixin


# many to many
books_in_users = db.Table("books_users",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id_user"), nullable=False),
    db.Column("book_id", db.Integer, db.ForeignKey("books.id_book"), nullable=False)
)


class Book(db.Model):
    __tablename__ = "books"
    id_book = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String(128), nullable=True)

    def __str__(self):
        return f"{self.book}"


@login_manager.user_loader
def current_user(id_user):
    return User.query.get(id_user)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    date_create = db.Column(db.DateTime, nullable=False)
    # number of users that have a determinate book
    books = db.relationship("Book", secondary=books_in_users, lazy=True,
                            backref=db.backref("users"))

    def get_id(self):
        return self.id_user

    def __str__(self):
        return f"{self.name}"
