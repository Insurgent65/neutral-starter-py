# Copyright (C) 2025 https://github.com/FranBarInstance/neutral-starter-py (See LICENCE)

"""Hello component routes module."""

import os

from flask import Response, request, send_from_directory
from hellocomp_0yt2sa import hellocomp


from app.config import Config
from core.dispatcher import Dispatcher

from . import bp  # pylint: disable=no-name-in-module
from .dispatcher_hellocomp import DispatcherHelloComp

STATIC = f"{bp.component['path']}/static"


# If business logic is needed, use custom route and dispatcher.
@bp.route("/test1", defaults={"route": "test1"}, methods=["GET"])
def test1(route) -> Response:
    """Handle test1 requests."""
    dispatch = DispatcherHelloComp(request, route, bp.neutral_route)
    dispatch.schema_local_data["message"] = hellocomp()
    dispatch.schema_data["dispatch_result"] = dispatch.test1()
    return dispatch.view.render()


# If not business logic is needed, use catch-all route and generic dispatcher.
@bp.route("/", defaults={"route": ""}, methods=["GET"])
@bp.route("/<path:route>", methods=["GET"])
def hellocomp_catch_all(route) -> Response:
    """Handle undefined urls."""

    # Can be a static file
    if route:
        file_path = os.path.join(STATIC, route)

        # If the route is a static file, return it
        if os.path.exists(file_path) and not os.path.isdir(file_path):
            response = send_from_directory(STATIC, route)
            response.headers["Cache-Control"] = Config.STATIC_CACHE_CONTROL
            return response

    # We use the generic dispatcher
    dispatch = Dispatcher(request, route, bp.neutral_route)
    dispatch.schema_local_data["message"] = hellocomp()

    # # In this case, it can also be done like this
    # dispatch = DispatcherHelloComp(request, route, bp.neutral_route)

    return dispatch.view.render()
