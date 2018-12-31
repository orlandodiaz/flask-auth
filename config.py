import os


class Config(object):
    pass

    
class ProdConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE')


class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Database settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'

    # Mailing settings
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = 1

    MAIL_USERNAME = os.environ.get('FLASK_MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('FLASK_MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('FLASK_DEFAULT_SENDER')


class TestConfig(Config):
    TESTING = True

    # Use an in-memory SQLITE database
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

