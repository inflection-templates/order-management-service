from tests.merchant.merchant_test_data import get_merchant_create_model, get_merchant_update_model
from tests.test_config import test_client
import json

def test_create_merchant(test_client):
    create_model = get_merchant_create_model()
    json_create_model = json.dumps(create_model, default=str)
    json_ = json.loads(json_create_model)
    response = test_client.post("/api/v1/merchants/",
                                headers = { "Content-Type": "application/json"},
                                json=json_)
    response_body = response.json()
    print(response_body)
    assert response.status_code == 201
    assert "id" in response_body["Data"]
    merchant_id = response_body["Data"]["id"]
    return merchant_id

def test_get_merchant_by_id(test_client):
    merchant_id = test_create_merchant(test_client)
    response = test_client.get(f"/api/v1/merchants/{merchant_id}")
    response_body = response.json()
    assert response.status_code == 200

def test_update_merchant(test_client):
    update_model = get_merchant_update_model()
    merchant_id = test_create_merchant(test_client)
    json_update_model = json.dumps(update_model, default=str)
    json_ = json.loads(json_update_model)
    response = test_client.put(f"/api/v1/merchants/{merchant_id}",
                               headers = { "Content-Type": "application/json"},
                                json=json_)
    response_body = response.json()
    assert response.status_code == 200

def test_delete_merchant(test_client):
    merchant_id = test_create_merchant(test_client)
    response = test_client.delete(f"/api/v1/merchants/{merchant_id}")
    response_body = response.json()
    assert response.status_code == 200
