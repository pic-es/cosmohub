import logging.config
import os

import sentry_sdk
import yaml
from flask import Flask
from flask import jsonify
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sqlalchemy.exc import IntegrityError

from sentry_sdk import last_event_id

from .config import config

log = logging.getLogger(__name__)

migrate = Migrate()
ma = Marshmallow()

# babel

# precommit
# black
# isort


def get_version():
    try:
        from setuptools_scm import get_version

        return get_version(root="..", relative_to=__file__)

    except ImportError: # pragma: no cover
        log.info("Cannot get version from setuptools_scm, as is not available.")
        from .version import version

        return version


def create_app(flask_env=None):
    # Load configuration
    flask_env = os.environ.get("FLASK_ENV", "development")
    config_class = config[flask_env]

    # Configure logging
    with open(config_class.LOG_CONFIG) as fd:
        log_config = yaml.safe_load(fd)
    logging.config.dictConfig(log_config)

    version = get_version()
    log.info("Initializing CosmoHub {}".format(version))

    app = Flask(__name__)
    app.config.from_object(config_class)

    from .database.model import db

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    from .api.users import users_blp

    app.register_blueprint(users_blp, url_prefix="/api")

    @app.errorhandler(400)
    def http_bad_request(error):
        return jsonify({"error": "bad request"}), 400

    @app.errorhandler(404)
    def http_not_found(error):
        return jsonify({"error": "not found"}), 404

    @app.errorhandler(422)
    def http_unprocessable_entity(error):
        return (
            jsonify({"error": "unprocessable entity", "details": error.exc.messages["json"]}),
            422,
        )

    @app.errorhandler(IntegrityError)
    def http_conflict(error):
        return jsonify({"error": "conflict"}), 409

    sentry_kwargs = {}
    if config_class.TESTING: # pragma: no branch
        sentry_kwargs['sample_rate'] = 0.0

    sentry_sdk.init(
        dsn=config_class.SENTRY_DSN,
        release="CosmoHub@{}".format(version),
        integrations=[FlaskIntegration(transaction_style="url"), SqlalchemyIntegration()],
        **sentry_kwargs
    )

    @app.errorhandler(500)
    def http_internal_error(error):
        return (
            jsonify(
                {"error": "internal server error", "event_id": last_event_id(), "sentry_dsn": config_class.SENTRY_DSN}
            ),
            500,
        )

    @app.route("/debug-sentry")
    def trigger_error():
        division_by_zero = 1 / 0

    return app
