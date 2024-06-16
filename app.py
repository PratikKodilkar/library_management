from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # adding configuration for using a sqlite database
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        from models import User, Book, Borrow
        db.create_all()

    from routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix='/api')

    return app
