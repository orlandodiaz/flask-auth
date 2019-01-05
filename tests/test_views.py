import os
import unittest

from myproject.users.models import User
from flask_login import current_user
from flask_testing import TestCase
from myproject import app, db


class TestIndexView(unittest.TestCase):

    def setUp(self):
        app.config.from_object('config.TestConfig')
        self.app = app.test_client()
        # self.app = app.test_client()
        # self.app.testing = True

        db.create_all()
        self.user = User(
            username="jason", email="test@gmail.com", full_name="jason")
        self.user.set_password('jason123')

        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_status_code(self):
        """ test the index (homepage) endpoint"""

        resp = self.app.get('/')

        self.assertEqual(resp.status_code, 302)

    def test_login_view(self):
        """ test the login endpoint"""

        resp = self.app.get('/users/login')

        self.assertEqual(resp.status_code, 200)

    def test_logout_view(self):
        """ Test the logout endpoint correctly stands """
        resp = self.app.get('/logout', follow_redirects=True)

        self.assertTrue(resp.status_code, 200)

    #
    def test_correct_login(self):
        with self.app:
            resp = self.app.post(
                '/users/login',
                data=dict(username="jason", password="jason123"),
                follow_redirects=True)

            self.assertTrue(current_user.is_authenticated)

    def test_incorrect_password_login(self):

        with self.app:
            resp = self.app.post(
                '/users/login',
                data=dict(username="jason", password="incorrectpassword"),
                follow_redirects=True)

            self.assertFalse(current_user.is_authenticated)

    def test_logout(self):
        with self.app:
            # self.app.post(
            #     '/users/login',
            #     data=dict(username="jason", password="jason123"),
            #     follow_redirects=True)

            self.app.get('/logout', follow_redirects=True)

            self.assertEqual(current_user.is_authenticated, False)

    def test_main_page_requires_login(self):
        resp = self.app.get('/users/profile', follow_redirects=True)

        self.assertNotIn(b'This is a demo', resp.data)


if __name__ == '__main__':
    unittest.main()
