from faker import Faker
from faker.providers import BaseProvider
import uuid

from app.domain_types.schemas.customer import CustomerCreateModel


def get_customer_create_model():
    fake = Faker()
    model = {
        "ReferenceId": uuid.uuid4(),
        "Name": fake.name(),
        "Email": fake.email(),
        "Phone": fake.phone_number().replace("-", ""),
    }
    print(model)
    return model
