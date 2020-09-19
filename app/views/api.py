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
    with open(os.path.join("app", "endpoint.json"), mode="r", encoding="utf-8") as fp:
        module_list = json.load(
            fp=fp
        )

    return Response(
        response=json.dumps(
            obj=dict(
                api=module_list
            )
        ),
        mimetype="application/json",
        status=200
    )
