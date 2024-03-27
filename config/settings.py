import os
from datetime import timedelta

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    FLASK_ENV = "development"
    SERVER_NAME = "localhost:8000"
    DEBUG = False
    TESTING = False
    REMEMBER_COOKIE_DURATION = timedelta(days=90)
    SECRET_KEY = os.getenv("SECRET_KEY", default="BAD_SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = (
        "postgresql://flaskblog:blogpassword@postgres:5432/flaskblog"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    FLASK_ENV = "production"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASEDIR, 'test.db')}"
    WTF_CSRF_ENABLED = False
