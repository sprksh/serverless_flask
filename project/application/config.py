import os


class BaseConfig(object):
    ENV = "local"
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret-key")

    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    LOG_ROOT = os.environ.get("LOG_ROOT", "/tmp/")

    DEBUG_TB_ENABLED = False
    CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SQLALCHEMY_DATABASE_URI = ''


class StageConfig(BaseConfig):
    ENV = "staging"
    DEBUG = False


class DevConfig(BaseConfig):
    ENV = "dev"
    DEBUG = True


class ProdConfig(BaseConfig):
    ENV = "prod"
    DEBUG = False
