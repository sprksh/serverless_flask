# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys
import os
import flask

from flask import Flask, render_template
from flask_admin import Admin, AdminIndexView

from application.extensions import (
    db,
    migrate,
)

from application.api.project_apis import project_bp
from application.exception import (
    ProjectValidationException,
    exception_handler,
    api_validation_exception_handler,
)
from application import commands
from application.services import admin as admin_views




def create_app(config):
    """An application factory, as explained here: https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config)
    configure_logging(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_commands(app)
    register_extensions(app)
    admin = Admin(app, index_view=AdminIndexView(url="/admin"))
    setup_admin(app, admin)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(project_bp)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_error_handlers(app):
    """

    :param app:
    :return:
    """
    app.register_error_handler(
        ProjectValidationException, api_validation_exception_handler
    )
    app.register_error_handler(Exception, exception_handler)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)


def setup_admin(app, admin):
    for admin_view in admin_views.__all__:
        model_view = getattr(admin_views, admin_view)
        admin.add_view(
            model_view(model_view._model, db.session, category=model_view._category)
        )


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)


class RequestIdFilter(logging.Filter):
    """
    This is a logging filter that makes the request ID available for use in the logging format.
    Note that we're checking if we're in a request context, as we may want to log things before
    Flask is fully loaded
    """

    def get_request_id(self):
        if getattr(flask.g, "request_id", None):
            return flask.g.request_id
        import uuid

        request_id = uuid.uuid4().hex
        flask.g.request_id = request_id
        return request_id

    def filter(self, record):
        record.request_id = self.get_request_id() if flask.has_request_context() else ""
        return True


def configure_logging(app):

    import logging.config

    environment = os.environ.get("ENV", "local")

    logging_conf = {
        "version": 1,
        "filters": {"request_id": {"()": "application.app.RequestIdFilter"}},
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "[%(asctime)s] %(levelname)s %(request_id)s - [%(name)s:%("
                "lineno)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "null": {
                "level": "DEBUG",
                "class": "logging.NullHandler",
                "formatter": "verbose",
                "filters": ["request_id"],
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
                "filters": ["request_id"],
            },
            "request": {
                "level": "DEBUG",
                "class": "logging.handlers.WatchedFileHandler",
                "filename": app.config["LOG_ROOT"] + "request.log",
                "formatter": "verbose",
                "filters": ["request_id"],
            },
        },
        "loggers": {
            "": {
                "handlers": ["console", "request"],
                "level": "INFO" if environment in ["prod", "stage"] else "DEBUG",
            },
            "request_handler": {
                "handlers": ["console", "request"],
                "level": "INFO" if environment in ["prod", "stage"] else "DEBUG",
                "propagate": True,
            },
        },
    }
    logging.config.dictConfig(logging_conf)
