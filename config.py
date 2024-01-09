from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv

from flask_cors import CORS

load_dotenv()

app = Flask (__name__)
db = SQLAlchemy(app)
CORS(app)

app_key = os.getenv('APP_KEY')
app_secret = os.getenv('APP_SECRET') 
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

db.init_app(app)
# conexao = 'mysql://root:BbdF6G5G6g665e6D3-BeHAAb5-C4hHe3@mysql.railway.internal:3306/railway'


migrate = Migrate(app, db)

app.config['SECRET_KEY'] = 'my-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:BbdF6G5G6g665e6D3-BeHAAb5-C4hHe3@monorail.proxy.rlwy.net:29587/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
