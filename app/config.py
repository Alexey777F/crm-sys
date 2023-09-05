from flask import Flask, Blueprint
import os
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    main = Blueprint('main', __name__)
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://" \
                                            f"{os.environ.get('POSTGRES_USER')}:" \
                                            f"{os.environ.get('POSTGRES_PASSWORD')}@" \
                                            f"{os.environ.get('PG_DB_HOST')}:5432/" \
                                            f"{os.environ.get('PG_DB_NAME')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True, "pool_recycle": 300}
    app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
    app.permanent_session_lifetime = datetime.timedelta(hours=10)
    db.init_app(app) # инициализация экземпляра SQLAlchemy для приложения Flask
    app.register_blueprint(main)
    return app, db
