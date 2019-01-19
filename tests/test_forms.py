from flaskauth.users.forms import LoginForm
from flaskauth import app, db
from log3 import log
from .test_base import BaseTestCase
import unittest


class TestLoginForm(unittest.TestCase):
    """ Test Login Form """

    def test_login_form_validates(self):

        with app.app_context():
            form = LoginForm(data={'username': 'admin', 'password': 'admin'})
            form.validate()
            for field, error in form.errors.items():
                log.info("{} - {}".format(field, error))

            self.assertTrue(form.validate())

    def test_login_form_fields_are_not_empty(self):

        with app.app_context():
            form = LoginForm(data={'username': 'admin', 'password': ''})
            form.validate()
            for field, error in form.errors.items():
                log.info("{} - {}".format(field, error))

            self.assertFalse(form.validate(), "Login form fields are empty")
