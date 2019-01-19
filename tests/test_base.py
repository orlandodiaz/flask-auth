import unittest

from flaskauth import app, db


class BaseTestCase(unittest.TestCase):
    """A base test case to inherit from."""

    # def create_app(self):
    #     app.config.from_object('config.TestConfiguration')
    #     return app

    def setUp(self):
        app.config.from_object('config.TestConfig')
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()