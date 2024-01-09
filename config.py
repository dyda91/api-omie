from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
import pymysql

load_dotenv()

app = Flask(__name__)
db = SQLAlchemy(app)

app_key = os.getenv('APP_KEY')
app_secret = os.getenv('APP_SECRET')
db_name = os.getenv('MYSQL_DB_NAME')
db_user = os.getenv('MYSQL_DB_USER')
db_password = os.getenv('MYSQL_DB_PASSWORD')
db_host = os.getenv('MYSQL_DB_HOST')

conexao = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}?charset=utf8mb4"
app.config['SECRET_KEY'] = 'my-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
db.init_app(app)
migrate = Migrate(app, db)












# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask
# from flask_migrate import Migrate
# from flask_login import LoginManager
# from flask_bcrypt import Bcrypt
# import os
# from dotenv import load_dotenv

# from flask_cors import CORS

# load_dotenv()

# app = Flask (__name__)
# db = SQLAlchemy(app)
# CORS(app)

# app_key = os.getenv('APP_KEY')
# app_secret = os.getenv('APP_SECRET') 
# conexao = os.getenv('SQLALCHEMY_DATABASE_URI') 
# bcrypt = Bcrypt(app)

# login_manager = LoginManager(app)

# db.init_app(app)
# # conexao = 'sqlite:///database.db'

# migrate = Migrate(app, db)

# app.config['SECRET_KEY'] = 'my-secret-key'
# app.config['SQLALCHEMY_DATABASE_URI'] = conexao
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
