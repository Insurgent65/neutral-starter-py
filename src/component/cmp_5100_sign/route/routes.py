"""This module handles the routing for sign-in, sign-up, and related forms."""

from flask import Response, request

from app.config import Config
from app.extensions import cache, limiter, require_header_set

from . import bp  # pylint: disable=no-name-in-module
from .dispatcher_form_sign import (
    DispatcherFormSign,
    DispatcherFormSignIn,
    DispatcherFormSignOut,
    DispatcherFormSignReminder,
    DispatcherFormSignUp,
)


@bp.route("/in", defaults={"route": "in"}, methods=["GET"])
def sign_in_get(route) -> Response:
    """Handle GET requests for login form."""
    dispatch = DispatcherFormSignIn(request, route, bp.neutral_route)
    dispatch.schema_data["dispatch_result"] = True
    return dispatch.view.render()


@bp.route("/in/form/<ltoken>", defaults={"route": "in/form"}, methods=["GET"])
def sign_in_form_get(route, ltoken) -> Response:
    """Handle GET requests for login form."""
    dispatch = DispatcherFormSignIn(request, route, bp.neutral_route, ltoken, "sign_in_form", "email")
    dispatch.schema_data["dispatch_result"] = dispatch.form_get()
    return dispatch.view.render()


@bp.route("/in/form/<ltoken>", defaults={"route": "in/form"}, methods=["POST"])
@limiter.limit(Config.SIGNIN_LIMITS, error_message="Please wait and try again later.")
def sign_in_form_post(route, ltoken) -> Response:
    """Handle POST requests for user authentication."""
    dispatch = DispatcherFormSignIn(request, route, bp.neutral_route, ltoken, "sign_in_form", "email")
    dispatch.schema_data["dispatch_result"] = dispatch.form_post()

    if dispatch.schema_data["dispatch_result"]:
        limiter.reset()

    return dispatch.view.render()


@bp.route("/up", defaults={"route": "up"}, methods=["GET"])
def sign_up_get(route) -> Response:
    """Handle GET requests for registration form."""
    dispatch = DispatcherFormSignUp(request, route, bp.neutral_route)
    dispatch.schema_data["dispatch_result"] = True
    return dispatch.view.render()


@bp.route("/up/form/<ltoken>", defaults={"route": "up/form"}, methods=["GET"])
def sign_up_form_get(route, ltoken) -> Response:
    """Handle GET requests for registration form."""
    dispatch = DispatcherFormSignUp(request, route, bp.neutral_route, ltoken, "sign_up_form", "email")
    dispatch.schema_data["dispatch_result"] = dispatch.form_get()
    return dispatch.view.render()


@bp.route("/up/form/<ltoken>", defaults={"route": "up/form"}, methods=["POST"])
@limiter.limit(Config.SIGNUP_LIMITS, error_message="Please wait and try again later.")
def sign_up_form_post(route, ltoken) -> Response:
    """Handle POST requests for new user registration."""
    dispatch = DispatcherFormSignUp(request, route, bp.neutral_route, ltoken, "sign_up_form", "email")
    dispatch.schema_data["dispatch_result"] = dispatch.form_post()
    return dispatch.view.render()


@bp.route("/reminder", defaults={"route": "reminder"}, methods=["GET"])
def sign_reminder_get(route) -> Response:
    """Handle GET requests for password reminder form."""
    dispatch = DispatcherFormSignReminder(request, route, bp.neutral_route)
    dispatch.schema_data["dispatch_result"] = True
    return dispatch.view.render()


@bp.route("/reminder/form/<ltoken>", defaults={"route": "reminder/form"}, methods=["GET"])
def sign_reminder_form_get(route, ltoken) -> Response:
    """Handle GET requests for password reminder form."""
    dispatch = DispatcherFormSignReminder(request, route, bp.neutral_route, ltoken, "sign_reminder_form", "email")
    dispatch.schema_data["dispatch_result"] = dispatch.form_get()
    return dispatch.view.render()


@bp.route("/reminder/form/<ltoken>", defaults={"route": "reminder/form"}, methods=["POST"])
@limiter.limit(Config.SIGNREMINDER_LIMITS, error_message="Please wait and try again later.")
@require_header_set("Requested-With-Ajax", "Require Ajax")
def sign_reminder_form_post(route, ltoken) -> Response:
    """Handle POST requests for password reminder form. Send reminder mail if successful."""
    dispatch = DispatcherFormSignReminder(request, route, bp.neutral_route, ltoken, "sign_reminder_form", "email")
    dispatch.schema_data["dispatch_result"] = dispatch.form_post()
    return dispatch.view.render()


@bp.route("/out", defaults={"route": "out"}, methods=["GET"])
def sign_out_get(route) -> Response:
    """Handle user logout and session cleanup."""
    dispatch = DispatcherFormSignOut(request, route, bp.neutral_route)
    dispatch.schema_data["dispatch_result"] = True
    return dispatch.view.render()


@bp.route("/out/form/<ltoken>", defaults={"route": "out/form"}, methods=["GET"])
@require_header_set("Requested-With-Ajax", "Require Ajax")
def sign_out_form(route, ltoken) -> Response:
    """Handle user logout and session cleanup."""
    dispatch = DispatcherFormSignOut(request, route, bp.neutral_route, ltoken)
    dispatch.schema_data["dispatch_result"] = dispatch.logout()
    return dispatch.view.render()


@bp.route("/pin/<pin_token>", defaults={"route": "pin"}, methods=["GET"])
def sign_pin_form_get(route, pin_token) -> Response:
    """Handle GET requests for PIN."""
    dispatch = DispatcherFormSignReminder(request, route, bp.neutral_route, pin_token)
    dispatch.schema_data["dispatch_result"] = dispatch.form_get()
    return dispatch.view.render()


@bp.route("/pin/<pin_token>", defaults={"route": "pin"}, methods=["POST"])
@limiter.limit(Config.SIGNT_LIMITS, error_message="Please wait and try again later.")
@require_header_set("Requested-With-Ajax", "Require Ajax")
def sign_pin_form_post(route, pin_token) -> Response:
    """Handle POST requests for new user registration."""
    dispatch = DispatcherFormSignUp(request, route, bp.neutral_route, pin_token, "email")
    dispatch.schema_data["dispatch_result"] = dispatch.form_post()
    return dispatch.view.render()


@bp.route("/help/<item>", defaults={"route": "help"}, methods=["GET"])
@require_header_set("Requested-With-Ajax", "Require Ajax")
@cache.cached(timeout=3600)
def sign_help_item(route, item) -> Response:
    """Serve cached help content for specific items."""
    dispatch = DispatcherFormSign(request, route, bp.neutral_route)
    dispatch.schema_data["help_item"] = item
    dispatch.schema_data["dispatch_result"] = True
    dispatch.view.response.headers["Cache-Control"] = Config.STATIC_CACHE_CONTROL
    return dispatch.view.render()
