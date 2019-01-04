import os


class Config(object):
    """ Default configuration for production and development"""

    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Mailing settings
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = 1

    MAIL_USERNAME = os.environ.get('FLASK_MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('FLASK_MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('FLASK_DEFAULT_SENDER')

    
class ProdConfig(Config):
    """ Configuration for production settings """

    ENV="production"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class DevConfig(Config):
    """ Configuration for development  """

    DEBUG = True
    ENV="development"


    # Database settings

    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/dev_postgres.db'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/dev_sqlite.db'

    POSTGRES = {
        'user': 'orr',
        'pw': '',
        'db': 'flaskauth',
        'host': 'localhost',
        'port': '5432',
    }
    SQLALCHEMY_DATABASE_URI= 'postgresql://%(user)s:\
    %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


class TestConfig(Config):
    """ Configuration for testing """
    TESTING = True

    # Use an in-memory SQLITE database
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

