# Criar app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config["SECRET_KEY"] = "b8a8697b8ed9b5fde245af36f0943462"
app.config["UPLOAD_FOLDER"] = "static/posts"
app.config['WTF_CSRF_ENABLED'] = True


database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homePage"

from fakePintrest import routes



