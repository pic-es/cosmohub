import os.path


class BaseConfig:
    SQLALCHEMY_ENGINE_OPTIONS = {"isolation_level": "SERIALIZABLE"}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    SENTRY_DSN = "https://d66be06c42dd46e9906158850445c917@sentry.io/4905309"


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = "postgresql://cosmohub@localhost/cosmohub"
    LOG_CONFIG = os.path.join(os.path.dirname(__file__), "logging_production.yaml")


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False

    SQLALCHEMY_DATABASE_URI = "postgresql://cosmohub@localhost/cosmohub_development"
    LOG_CONFIG = os.path.join(os.path.dirname(__file__), "logging_development.yaml")


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "postgresql://cosmohub@localhost/cosmohub_testing"
    LOG_CONFIG = os.path.join(os.path.dirname(__file__), "logging_development.yaml")


class CIConfig(TestingConfig):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres@localhost/cosmohub_ci"


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "ci": CIConfig,
}
