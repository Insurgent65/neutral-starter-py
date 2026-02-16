"""
Basic tests for application setup and routing.
"""


def test_app_is_created(flask_app):
    """Test that the app instance is created with the correct name."""
    assert flask_app.name == "app"


def test_config_is_loaded(flask_app):
    """Test that the test configuration is loaded correctly."""
    assert flask_app.config["TESTING"] is True
    assert flask_app.config["SECRET_KEY"] == "test_secret_key"


def test_index_page(client):
    """
    Test routing for index page.
    Verifies that / is accessible.
    """
    response = client.get("/")
    assert response.status_code == 200


def test_rejects_disallowed_host(client):
    """Requests with disallowed Host must return 400."""
    response = client.get("/", headers={"Host": "evil.example"})
    assert response.status_code == 400


def test_accepts_allowed_host(client):
    """Requests with allowed Host must continue normally."""
    response = client.get("/", headers={"Host": "localhost"})
    assert response.status_code == 200


def test_referrer_policy_header_default(client):
    """Referrer-Policy must be sent with the configured default value."""
    response = client.get("/")
    assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"


def test_components_loaded(flask_app):
    """Test that components are correctly identified and loaded."""
    if hasattr(flask_app, "components") and flask_app.components:
        print("\nLoaded Components:", list(flask_app.components.collection.keys()))
        assert len(flask_app.components.collection) > 0
