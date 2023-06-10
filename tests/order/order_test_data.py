from faker import Faker
from faker.providers import BaseProvider
import uuid

from app.domain_types.schemas.order import OrderCreateModel

def get_order_create_model():
    fake = Faker()
    model = {
        "OrderTypeId": uuid.uuid4(),
        "CustomerId": uuid.uuid4(),
        "CartId": uuid.uuid4(),
        "TipApplicable": fake.pybool(),
        "Notes": fake.text(),
        "OrderLineItems": None
    }
    return model
