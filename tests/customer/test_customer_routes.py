from tests.customer.customer_test_data import get_customer_create_model
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
    assert response.status_code == 201


