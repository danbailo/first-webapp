from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from app import filters

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, static_folder="../public")
    app.config["SECRET_KEY"] = "DontTellAnyone"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.jinja_env.filters["format_date"] = filters.format_date
    app.jinja_env.filters["len"] = len

    db.init_app(app)
    login_manager.init_app(app)

    from app import routes
    routes.init_app(app)

    return app
