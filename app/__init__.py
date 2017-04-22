from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

STATIC_FOLDER = 'static/'

UPLOAD_FOLDER = 'static/img/products/'
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg'])

app = Flask(__name__, static_folder='static/')

app.secret_key = 'godis'

app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)

from app import views, models
