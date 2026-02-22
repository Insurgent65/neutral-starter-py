"""Dev Admin routes."""

from flask import Response, request

from . import bp  # pylint: disable=no-name-in-module
from .dispatcher_dev_admin import DispatcherDevAdmin


@bp.route("/", defaults={"route": ""}, methods=["GET", "POST"])
@bp.route("/<path:route>", methods=["GET", "POST"])
def index(route) -> Response:
    """Dev Admin page for config.db custom overrides."""
    dispatch = DispatcherDevAdmin(request, route, bp.neutral_route)
    return dispatch.render_route()
