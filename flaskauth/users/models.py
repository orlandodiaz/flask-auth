from flask_sqlalchemy import SQLAlchemy
from flaskauth import app
from flask_login import UserMixin
from flaskauth import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flaskauth import db
import jwt
from time import time
from flaskauth.users.email import threaded_email_send
from flask_mail import Message
from flask import render_template
from flask_login import current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(64), nullable=False, index=True)

    password = db.Column(db.String(128))

    is_verified = db.Column(db.Boolean(), default=False)

    def send_verification_email(self):
        token = self.get_verify_email_token()

        msg = Message(
            "Verify your email",
            recipients=[self.email],
            body=render_template(
                'email/email_verification.txt', user=self, token=token))
        threaded_email_send(msg)

    def get_verify_email_token(self, expires_in=600):
        return jwt.encode({
            'verify_email_token': self.id,
            'exp': time() + expires_in
        },
                          app.config['SECRET_KEY'],
                          algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_email_token(token):
        try:
            id = jwt.decode(
                token, app.config['SECRET_KEY'],
                algorithms=['HS256'])['verify_email_token']
        except:
            return
        return User.query.get(id)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({
            'reset_password': self.id,
            'exp': time() + expires_in
        },
                          app.config['SECRET_KEY'],
                          algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, app.config['SECRET_KEY'],
                algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return "<{}>".format(self.username)

    def __str__(self):
        return self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # def get_id(self):
    #     return str(self.id)
    #
    # def is_authenticated(self):
    #     return True

    #
    # def is_active(self):
    #     return self.is_active()
    #
    # def is_anonymous(self):
    #     return False
    # if self.username == current_user.username:
    #     return current_user.is_authenticated
    # else:
    #     return False

    # @property
    # def password(self):
    #     raise AttributeError('PW is not a readable attribute')
    #
    # @password.setter
    # def password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    # def verify_password(self, password):
    #     return check_password_hash(self.password_hash, password)
