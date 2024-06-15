from flask import Flask
from config import db
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'instance', 'library_database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

db.init_app(app)

def register_blueprints(app):
    from routes.users import users_bp
    app.register_blueprint(users_bp)

register_blueprints(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)