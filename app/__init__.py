# -*- coding: utf-8 -*-
from json import dumps
from os import listdir, path

from flask import Flask, Response


def create_app():
    app = Flask(__name__)

    module_list = []

    for vp in listdir(path.join("app", "views")):
        if not vp.startswith("__") and vp.endswith(".py"):
            file_name = vp.split(".py")[0]
            try:
                obj = getattr(getattr(__import__(f"app.views.{file_name}"), "views"), file_name)

                app.register_blueprint(
                    blueprint=getattr(obj, "bp")
                )

                module_list.append(
                    dict(
                        code=file_name,
                        name=getattr(obj, "NAME")
                    )
                )
            except AttributeError:
                print(f"[!] '{file_name}' is not view point")

    @app.route("/")
    def show_available():
        return Response(
            response=dumps(obj=module_list),
            mimetype="application/json",
            status=200
        )

    return app
