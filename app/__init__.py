# -*- coding: utf-8 -*-

import os
import json
import importlib

from flask import Flask


def create_app():
    app = Flask(__name__)

    # Show available api
    from .views import api
    app.register_blueprint(api.bp)

    # Api Endpoint
    module_list = []
    for m in os.listdir(os.path.join("app", "api")):
        if not m.startswith("__") and m.endswith(".py"):
            module = importlib.import_module(
                name=f"app.api.{m.split('.py')[0]}"
            )

            try:
                module.__getattribute__("track_parcel")
                module.__getattribute__("last")
                name = module.__getattribute__("NAME")

                app.register_blueprint(
                    blueprint=module.__getattribute__("bp")
                )

                print(f"+ {m} -> '{name}'")
                module_list.append(
                    dict(
                        code=m.split('.py')[0],
                        name=name
                    )
                )
            except AttributeError:
                print(f"- '{m}' is not registered")

    with open(os.path.join("app", "endpoint.json"), mode="w", encoding="utf-8") as fp:
        json.dump(
            obj=module_list,
            fp=fp
        )

    print("-"*30)
    return app
