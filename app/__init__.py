from flask import Flask
from config import DevConfig
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(DevConfig)

mail = Mail(app)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


login_manager = LoginManager()
login_manager.init_app(app)

migrate = Migrate(app, db)


from app.main.routes import main
from app.users.routes import users



app.register_blueprint(main)
app.register_blueprint(users)



