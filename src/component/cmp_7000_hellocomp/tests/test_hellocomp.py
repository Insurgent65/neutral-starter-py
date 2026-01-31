# Copyright (C) 2025 https://github.com/FranBarInstance/neutral-starter-py (See LICENCE)

"""
Tests for the hellocomp component.

These tests verify the routes and dispatcher of the Hello Component.
The component is mounted at /hello-component and defines routes for:
- / (index via catch-all)
- /test1 (specific route with DispatcherHelloComp)
- /<path> (catch-all for undefined routes)
"""

import os
from flask import request

# These imports work thanks to the sys.path manipulation in __init__.py
from route.dispatcher_hellocomp import DispatcherHelloComp
from core.dispatcher import Dispatcher

# Determine paths dynamically
_test_dir = os.path.dirname(os.path.abspath(__file__))
_comp_dir = os.path.dirname(_test_dir)
_comp_name = os.path.basename(_comp_dir)
_neutral_route = os.path.join(_comp_dir, "neutral", "route")


class TestHelloCompRoutes:
    """Tests for Hello Component routes."""

    def test_hellocomp_route_exists(self, flask_app):
        """Test that the component blueprint is registered."""
        # The blueprint name is derived from the folder name: bp_cmp_XXXX_hellocomp
        bp_name = f"bp_{_comp_name}"
        assert bp_name in flask_app.blueprints

    def test_hellocomp_test1_route_defined(self, flask_app):
        """Test that the test1 route handler is defined."""
        # Get the actual route prefix from the blueprint manifest
        bp_name = f"bp_{_comp_name}"
        route_prefix = flask_app.blueprints[bp_name].url_prefix

        rules = [rule.rule for rule in flask_app.url_map.iter_rules()]
        assert f"{route_prefix}/test1" in rules


class TestDispatcherHelloComp:
    """Tests for DispatcherHelloComp class."""

    def test_dispatcher_test1_returns_true(self, flask_app):
        """Test that DispatcherHelloComp.test1() returns True."""
        bp_name = f"bp_{_comp_name}"
        route_prefix = flask_app.blueprints[bp_name].url_prefix

        with flask_app.test_request_context(f"{route_prefix}/test1"):
            dispatcher = DispatcherHelloComp(request, "test1", _neutral_route)
            result = dispatcher.test1()

            assert result is True

    def test_dispatcher_sets_foo_in_schema_local_data(self, flask_app):
        """Test that DispatcherHelloComp sets 'foo' in schema_local_data."""
        bp_name = f"bp_{_comp_name}"
        route_prefix = flask_app.blueprints[bp_name].url_prefix

        with flask_app.test_request_context(f"{route_prefix}/"):
            dispatcher = DispatcherHelloComp(request, "", _neutral_route)

            assert "foo" in dispatcher.schema_local_data
            assert dispatcher.schema_local_data["foo"] == "bar"

    def test_dispatcher_inherits_from_base_dispatcher(
        self, flask_app  # pylint: disable=unused-argument
    ):
        """Test that DispatcherHelloComp inherits from Dispatcher."""
        assert issubclass(DispatcherHelloComp, Dispatcher)
