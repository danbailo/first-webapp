from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


from app.utils import format_date

db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__, static_folder="static")
    app.config["SECRET_KEY"] = "DontTellAnyone"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.jinja_env.filters["format_date"] = format_date
    app.jinja_env.filters["len"] = len

    db.init_app(app=app)
    login_manager.init_app(app=app)
    bootstrap.init_app(app=app)

    from app import routes
    routes.init_app(app=app)

    db.create_all(app=app)

    return app
