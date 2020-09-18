# -*- coding: utf-8 -*-

import os
import importlib

from flask import Flask


def create_app():
    app = Flask(__name__)

    # Show available api
    from .views import api
    app.register_blueprint(api.bp)

    # Api Endpoint
    for m in os.listdir(os.path.join("app", "api")):
        if not m.startswith("__") and m.endswith(".py"):
            module = importlib.import_module(
                name=f"app.api.{m.split('.py')[0]}"
            )

            app.register_blueprint(
                blueprint=module.__getattribute__("bp")
            )

    return app
