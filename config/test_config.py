from config.settings import TestConfig

class TestConfigOverride(TestConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'