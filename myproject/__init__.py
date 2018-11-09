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

from .users.models import User

from flask_admin import Admin


from myproject.admin.views import AdminView
from myproject.admin.views import MyAdminIndexView

admin_page = Admin(app, name='Admin page',
                   template_mode='bootstrap3',
                   index_view=MyAdminIndexView())

admin_page.add_view(AdminView(User, db.session))

from myproject.main.views import main
from myproject.users.views import users
from myproject.admin.views import admin1


app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(admin1)


