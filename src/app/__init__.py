from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from app.utils import format_date

db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap()
mail = Mail()


def create_app():
    app = Flask(__name__, static_folder="static")
    app.config["SECRET_KEY"] = "DontTellAnyone"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_DEBUG"] = True
    app.config["MAIL_USERNAME"] = "YOUR_USERNAME"
    app.config["MAIL_PASSWORD"] = "YOUR_PASSWORD"
    app.config["MAIL_DEFAULT_SENDER"] = 'YOU <YOUR_EMAIL>'
    app.jinja_env.filters["format_date"] = format_date
    app.jinja_env.filters["len"] = len

    db.init_app(app=app)
    login_manager.init_app(app=app)
    bootstrap.init_app(app=app)
    mail.init_app(app=app)

    from app import views
    views.init_app(app=app)

    db.create_all(app=app)

    return app
