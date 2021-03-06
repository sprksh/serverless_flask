# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# from flask_webpack import Webpack
# from flask_wtf.csrf import CSRFProtect

# bcrypt = Bcrypt()
# csrf_protect = CSRFProtect()
# login_manager = LoginManager()
db = SQLAlchemy(session_options={"autocommit": False})
migrate = Migrate()
# cache = Cache()
# debug_toolbar = DebugToolbarExtension()
# webpack = Webpack()
