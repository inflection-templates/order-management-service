from tests.customer.customer_test_data import get_customer_create_model, get_customer_update_model
from tests.test_config import test_client
import json

def test_create_customer(test_client):
    create_model = get_customer_create_model()
    json_create_model = json.dumps(create_model, default=str)
    json_ = json.loads(json_create_model)
    response = test_client.post("/api/v1/customers/",
                                headers = { "Content-Type": "application/json"},
                                json=json_)
    response_body = response.json()
    print(response_body)
    assert response.status_code == 201
    assert "id" in response_body["Data"]
    customer_id = response_body["Data"]["id"]
    return customer_id

def test_get_customer_by_id(test_client):
    customer_id = test_create_customer(test_client)
    response = test_client.get(f"/api/v1/customers/{customer_id}")
    response_body = response.json()
    assert response.status_code == 200

def test_update_customer(test_client):
    update_model = get_customer_update_model()
    customer_id = test_create_customer(test_client)
    json_update_model = json.dumps(update_model, default=str)
    json_ = json.loads(json_update_model)
    response = test_client.put(f"/api/v1/customers/{customer_id}",
                               headers = { "Content-Type": "application/json"},
                                json=json_)
    response_body = response.json()
    assert response.status_code == 200

def test_delete_customer(test_client):
    customer_id = test_create_customer(test_client)
    response = test_client.delete(f"/api/v1/customers/{customer_id}")
    response_body = response.json()
    assert response.status_code == 200
