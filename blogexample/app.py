#!/usr/bin/env python

from flask import Flask, render_template, session, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy

from werkzeug.debug import DebuggedApplication

# from flask_ckeditor import CKEditor#, CKEditorField


db = SQLAlchemy()
# ckeditor = CKEditor()


# app.py

def create_app(config_object=None):
    """Create an application."""
    app = Flask(__name__)

    if config_object is None:
        app.config.from_object('config.settings')
    else:
        app.config.from_object(config_object)

    from blogexample.blueprints.blog import blog
    app.register_blueprint(blog)

    db.init_app(app)

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)
    
    return app


