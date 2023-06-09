import pytest
from fastapi.testclient import TestClient
from app.startup.application import get_application


@pytest.fixture(scope="module")
def test_client():
    app = get_application()
    client = TestClient(app)
    yield client
