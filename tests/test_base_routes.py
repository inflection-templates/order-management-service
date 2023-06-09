from tests.test_config import test_client

def test_root_route(test_client):
    response = test_client.get("/")
    assert response.status_code == 200

def test_healthcheck_route(test_client):
    response = test_client.get("/health-check")
    assert response.status_code == 200
