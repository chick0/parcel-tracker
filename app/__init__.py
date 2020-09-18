# -*- coding: utf-8 -*-

import os
import importlib

from flask import Flask


def create_app():
    app = Flask(__name__)

    # API
    for m in os.listdir(os.path.join("app", "views")):
        if not m.startswith("__"):
            module = importlib.import_module(
                name=f"app.views.{m.split('.py')[0]}"
            )

            app.register_blueprint(
                blueprint=module.__getattribute__("bp")
            )

    return app
