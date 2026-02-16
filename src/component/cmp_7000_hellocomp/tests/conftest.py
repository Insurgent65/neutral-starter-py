# Copyright (C) 2025 https://github.com/FranBarInstance/neutral-starter-py (See LICENCE)

"""
Pytest configuration and fixtures for hellocomp component.

This conftest provides the necessary fixtures for component tests.
When the component is distributed independently, these fixtures
allow testing without the main application's test configuration.
"""

import os
import sys

import pytest

from app import create_app
from app.config import Config

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_COMP_DIR = os.path.dirname(_BASE_DIR)
_ROUTE_DIR = os.path.join(_COMP_DIR, "route")

if _ROUTE_DIR not in sys.path:
    sys.path.insert(0, _ROUTE_DIR)


class TestConfig(Config):
    """
    Configuration for testing purposes.
    Uses in-memory databases and dummy mail settings.
    """

    TESTING = True
    SECRET_KEY = "test_secret_key"
    # Use memory databases for isolation
    DB_PWA = "sqlite:///:memory:"
    DB_SAFE = "sqlite:///:memory:"
    DB_FILES = "sqlite:///:memory:"
    # Disable features that might require external services
    MAIL_METHOD = "dummy"


@pytest.fixture(name="flask_app")
def fixture_flask_app():
    """
    Create and configure a new Flask app instance for each test.
    """
    app = create_app(TestConfig, debug=True)

    yield app

    # Teardown: Remove component modules to force reload in next test
    for module in list(sys.modules.keys()):
        if module.startswith("component."):
            del sys.modules[module]


@pytest.fixture
def client(flask_app):  # pylint: disable=redefined-outer-name
    """
    A test client for the app.
    """
    return flask_app.test_client()


@pytest.fixture
def runner(flask_app):  # pylint: disable=redefined-outer-name
    """
    A test CLI runner for the app.
    """
    return flask_app.test_cli_runner()
