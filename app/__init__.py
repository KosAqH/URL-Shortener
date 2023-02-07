from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'this-shouldnt-be-here-in-real-app'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)

from app.models import URL

# blueprint for non-auth parts of app
from app.main import main as main_blueprint
app.register_blueprint(main_blueprint)

with app.app_context():
    db.create_all()