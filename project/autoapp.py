# -*- coding: utf-8 -*-
"""Create an application instance."""
import os
from application.app import create_app
from application import config


class FlaskEnvironment(object):
    env = os.environ.get("ENV", "local")
    __instance = None

    def __init__(self,):
        if not FlaskEnvironment.__instance:
            FlaskEnvironment.__instance = super(FlaskEnvironment, self).__init__()


class MainApp(object):
    flask_env = FlaskEnvironment()

    @staticmethod
    def get_app():
        conf = config.BaseConfig
        if str(MainApp.flask_env.env).lower() == "prod":
            conf = config.ProdConfig
        elif str(MainApp.flask_env.env).lower() == "staging":
            conf = config.StageConfig
        elif str(MainApp.flask_env.env).lower() == "dev":
            conf = config.DevConfig
        return create_app(conf)


app = MainApp().get_app()
