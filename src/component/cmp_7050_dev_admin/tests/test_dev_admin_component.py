"""Tests for dev-admin component."""

import json
from pathlib import Path

from app.config_db import get_component_custom_override

_TEST_DIR = Path(__file__).resolve().parent
_COMP_DIR = _TEST_DIR.parent
_BP_NAME = f"bp_{_COMP_DIR.name}"


def _route_prefix(flask_app) -> str:
    return flask_app.blueprints[_BP_NAME].url_prefix or ""


def _route(flask_app, suffix: str) -> str:
    return f"{_route_prefix(flask_app)}{suffix}"


def test_dev_admin_blueprint_registered(flask_app):
    """Component blueprint should be registered using folder name."""
    assert _BP_NAME in flask_app.blueprints


def test_dev_admin_rejects_non_local_ip(client):
    """Route must reject non-local IPs by default."""
    client.application.config["DEV_ADMIN_USER"] = "admin"
    client.application.config["DEV_ADMIN_PASSWORD"] = "secret"
    response = client.get(_route(client.application, "/"), environ_base={"REMOTE_ADDR": "8.8.8.8"})
    assert response.status_code == 403


def test_dev_admin_login_page(client, tmp_path):
    """Login form should render when credentials are configured."""
    client.application.config["DEV_ADMIN_USER"] = "admin"
    client.application.config["DEV_ADMIN_PASSWORD"] = "secret"
    client.application.config["CONFIG_DB_PATH"] = str(tmp_path / "config.db")

    response = client.get(_route(client.application, "/"), environ_base={"REMOTE_ADDR": "127.0.0.1"})
    assert response.status_code == 200
    assert b"Dev Admin Login" in response.data


def test_dev_admin_login_and_save_override(client, tmp_path):
    """After login, admin should save custom override into config.db."""
    db_path = tmp_path / "config.db"
    client.application.config["DEV_ADMIN_USER"] = "admin"
    client.application.config["DEV_ADMIN_PASSWORD"] = "secret"
    client.application.config["CONFIG_DB_PATH"] = str(db_path)

    with client.session_transaction() as sess:
        sess["DEV_ADMIN_CSRF"] = "csrf-test-token"

    login = client.post(
        _route(client.application, "/"),
        data={
            "action": "login",
            "username": "admin",
            "password": "secret",
            "csrf_token": "csrf-test-token",
        },
        environ_base={"REMOTE_ADDR": "127.0.0.1"},
    )
    assert login.status_code == 200
    assert b"Custom Overrides" in login.data

    payload = {
        "manifest": {"route": "/hello-from-dev-admin"},
        "schema": {"data": {"from_dev_admin": True}},
    }
    save = client.post(
        _route(client.application, "/"),
        data={
            "action": "save",
            "comp_uuid": "hellocomp_0yt2sa",
            "override_json": json.dumps(payload),
            "enabled": "1",
            "csrf_token": "csrf-test-token",
        },
        environ_base={"REMOTE_ADDR": "127.0.0.1"},
    )
    assert save.status_code == 200
    assert b"Override saved." in save.data

    stored = get_component_custom_override(str(db_path), "hellocomp_0yt2sa")
    assert stored == payload


def test_dev_admin_rejects_post_without_valid_csrf(client, tmp_path):
    """POST actions must be rejected with invalid CSRF token."""
    client.application.config["DEV_ADMIN_USER"] = "admin"
    client.application.config["DEV_ADMIN_PASSWORD"] = "secret"
    client.application.config["CONFIG_DB_PATH"] = str(tmp_path / "config.db")

    with client.session_transaction() as sess:
        sess["DEV_ADMIN_CSRF"] = "expected-token"

    response = client.post(
        _route(client.application, "/"),
        data={"action": "login", "username": "admin", "password": "secret", "csrf_token": "bad-token"},
        environ_base={"REMOTE_ADDR": "127.0.0.1"},
    )
    assert response.status_code == 200
    assert b"Invalid CSRF token." in response.data
