from faker import Faker
from faker.providers import BaseProvider
import uuid

from app.domain_types.schemas.merchant import MerchantCreateModel, MerchantUpdateModel

def get_merchant_create_model():
    fake = Faker()
    model = {
        "ReferenceId": uuid.uuid4(),
        "Name": fake.name(),
        "Email": fake.email(),
        "Phone": fake.phone_number().replace("-", "")[:12],
    }
    print(model)
    return model

def get_merchant_update_model():
    fake = Faker()
    model = {
        "Name": fake.name(),
        "Email": fake.email(),
        "Phone": fake.phone_number().replace("-", "")[:12],
    }
    print(model)
    return model
