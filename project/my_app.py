from flask import Flask
import os
import datetime
from models import db


class CreateApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://" \
                                                     f"{os.environ.get('POSTGRES_USER')}:" \
                                                     f"{os.environ.get('POSTGRES_PASSWORD')}@" \
                                                     f"{os.environ.get('PG_DB_HOST')}:5432/" \
                                                     f"{os.environ.get('PG_DB_NAME')}"
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True, 'pool_recycle': 300}
        self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        self.app.permanent_session_lifetime = datetime.timedelta(hours=10)
        db.init_app(self.app)

    def return_app(self):
        return self.app
