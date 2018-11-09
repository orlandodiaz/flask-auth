from flask_login import current_user
from flask import redirect, url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView

from flask import Blueprint

admin1 = Blueprint('adminpanel', __name__)


class AdminView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        print('redirecting')
        return redirect(url_for('users.login', next=request.url))


class MyAdminIndexView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        print('redirecting')
        return redirect(url_for('users.login', next=request.url))