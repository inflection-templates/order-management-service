import pytest
from fastapi.testclient import TestClient
from app.startup.application import app

@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client
