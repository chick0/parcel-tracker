# -*- coding: utf-8 -*-

import os
import json
import importlib

from flask import Blueprint, Response

bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix="/"
)


@bp.route("/")
def show_available():
    api_list = os.listdir(os.path.join("app", "api"))
    module_list = []

    for item in api_list:
        if not item.startswith("__") and item.endswith(".py"):
            module = importlib.import_module(
                name=f"app.api.{item.split('.py')[0]}"
            )

            try:
                module_list.append(
                    dict(
                        code=item.split('.py')[0],
                        name=module.__getattribute__("NAME")
                    )
                )
            except AttributeError:
                pass

    return Response(
        response=json.dumps(
            obj=dict(
                api=module_list
            )
        ),
        mimetype="application/json",
        status=200
    )
