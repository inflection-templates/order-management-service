import uuid
from app.common.utils import print_colorized_json
from app.domain_types.order import OrderCreateModel, OrderResponseModel


def create_order(model: OrderCreateModel) -> OrderResponseModel:
    order = OrderResponseModel(**model.dict(), id=uuid.uuid4(), DisplayCode="1234", InvoiceNumber="1234")
    print_colorized_json(order)
    return order

