from datetime import timedelta

DEBUG = True

SERVER_NAME = 'localhost:8000'
SECRET_KEY = 'insecurekeyfordev'


# SQLAlchemy.
db_uri = 'postgresql://flaskblog:blogpassword@postgres:5432/flaskblog'
SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False

REMEMBER_COOKIE_DURATION = timedelta(days=90)


class TestConfig:
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test-secret'
