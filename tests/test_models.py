from myproject.users.forms import LoginForm
from myproject import app, db
from log3 import log
from .test_base import BaseTestCase
import unittest
from myproject.users.models import User


class TestUserModel(unittest.TestCase):
    """ Test User Model """

    def setUp(self):
        app.config.from_object('config.TestConfig')
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        """Create user test """

        user = User(
            username="myusername",
            password="mypassword",
            email="myemail@gmail.com",
            full_name="myname")
        db.session.add(user)
        db.session.commit()

        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.__str__(), user.username)

    def test_password_is_hashed(self):
        user = User()
        user.set_password("mypassword")

        self.assertNotEquals(user.password, "mypassword")
