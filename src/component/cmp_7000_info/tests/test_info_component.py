"""Tests for the info component."""

from pathlib import Path

_TEST_DIR = Path(__file__).resolve().parent
_COMP_DIR = _TEST_DIR.parent
_BP_NAME = f"bp_{_COMP_DIR.name}"


def _route_prefix(flask_app) -> str:
    return flask_app.blueprints[_BP_NAME].url_prefix or ""


def _route(flask_app, suffix: str) -> str:
    return f"{_route_prefix(flask_app)}{suffix}"


def test_info_blueprint_registered(flask_app):
    """Component blueprint should be registered using folder name."""
    assert _BP_NAME in flask_app.blueprints


def test_info_catch_all_route_responds(client):
    """Info catch-all route should render configured pages."""
    response = client.get(_route(client.application, "/help"))
    assert response.status_code == 200

