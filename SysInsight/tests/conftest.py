"""
pytest configuration and fixtures
"""
import pytest
from app import create_app

@pytest.fixture
def app():
    """Create application instance for testing"""
    app = create_app('testing')
    yield app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create CLI test runner"""
    return app.test_cli_runner()
