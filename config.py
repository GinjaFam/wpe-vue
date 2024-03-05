class Config(object):
    SESSION_COOKIE_NAME = 'wpe_app_session'
    SECRET_KEY = 'admin'

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_DEBUG = True
    DBNAME='app'
    DBHOST='localhost'
    DBUSER='app_user'
    DBPASS='app_password'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///wpe-dev.db'
    SQLALCHEMY_ECHO = True
    DATABASE_URI = f"postgresql+psycopg2://{DBUSER}:{DBPASS}@{DBHOST}/{DBNAME}"
    SQLALCHEMY_DATABASE_URI= 'postgresql://app_user:app_password@db:5432/app'
    TEST_DATABASE_URI = f"postgresql+psycopg2://{DBUSER}:{DBPASS}@localhost/{DBNAME}"
    JWT_SECRET_KEY = '\xc3\x13\x06E<\xa2\xf4=lFT\x94\x81\xde\xe6\xaf\x1d\xf9s\xac$\xb2\x000'
    
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/production'
    # Additional production-specific settings

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for tests
    # Additional testing-specific settings