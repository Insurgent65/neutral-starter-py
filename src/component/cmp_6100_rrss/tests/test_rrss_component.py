"""Tests for the rrss component."""

import importlib
from pathlib import Path

from flask import request

_TEST_DIR = Path(__file__).resolve().parent
_COMP_DIR = _TEST_DIR.parent
_BP_NAME = f"bp_{_COMP_DIR.name}"


def _route_prefix(flask_app) -> str:
    return flask_app.blueprints[_BP_NAME].url_prefix or ""


def _route(flask_app, suffix: str) -> str:
    return f"{_route_prefix(flask_app)}{suffix}"


def test_rrss_blueprint_registered(flask_app):
    """Component blueprint should be registered using folder name."""
    assert _BP_NAME in flask_app.blueprints


def test_rrss_ajax_requires_header(client):
    """AJAX feed endpoint should reject non-AJAX requests."""
    response = client.get(_route(client.application, "/ajax/myfeed"))
    assert response.status_code == 403


def test_rrss_dispatcher_set_rss_name(client):
    """Dispatcher should accept configured names and reject unknown names."""
    endpoint = f"{_BP_NAME}.rrss"
    module = importlib.import_module(client.application.view_functions[endpoint].__module__)
    schema = {
        "inherit": {
            "data": {
                "rsss_default": "default_feed",
                "rrss_urls": {"tech": "https://example.org/rss"},
            }
        }
    }
    prefix = _route_prefix(client.application)

    with client.application.test_request_context(f"{prefix}/"):
        dispatcher = module.DispatcherRrss(request, "", "")

        assert dispatcher.set_rss_name(schema) is True
        assert dispatcher.schema_data["rrss_name"] == "default_feed"

        assert dispatcher.set_rss_name(schema, "tech") is True
        assert dispatcher.schema_data["rrss_name"] == "tech"

        assert dispatcher.set_rss_name(schema, "unknown") is False
        assert dispatcher.schema_data["rrss_name"] == ""
