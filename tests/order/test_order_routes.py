from tests.order.order_test_data import get_order_create_model
from tests.test_config import test_client
import json

def test_create_order(test_client):
    create_model = get_order_create_model()
    json_create_model = json.dumps(create_model, default=str) 
    json_ = json.loads(json_create_model)
    response = test_client.post("/api/v1/orders/", 
                                headers = { "Content-Type": "application/json"}, 
                                json=json_)
    response_body = response.json()
    assert response.status_code == 201



