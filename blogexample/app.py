#!/usr/bin/env python

import os

from flask import Flask, jsonify, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.debug import DebuggedApplication

# from flask_ckeditor import CKEditor#, CKEditorField


db = SQLAlchemy()
# ckeditor = CKEditor()


def create_app(main=True, debug=True):
    """Create an application."""
    app = Flask(__name__)

    config_type = os.getenv("CONFIG_TYPE", default="config.settings.DevelopmentConfig")
    app.config.from_object(config_type)

    from blogexample.blueprints.blog import blog

    app.register_blueprint(blog)

    db.init_app(app)
    # ckeditor.init_app(app)

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    return app
