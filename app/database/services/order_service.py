import uuid
from app.common.utils import print_colorized_json
from sqlalchemy.orm import Session
from app.domain_types.schemas.order import OrderCreateModel, OrderResponseModel


def create_order(session: Session, model: OrderCreateModel) -> OrderResponseModel:
    try:
        order = session.db.add(model)
        session.db.commit()
        session.db.refresh(model)
    except Exception as e:
        print(e)
        session.db.rollback()
        raise e
    finally:
        session.db.close()

    # order = OrderResponseModel(**model.dict(), id=uuid.uuid4(), DisplayCode="1234", InvoiceNumber="1234")
    print_colorized_json(order)
    return order

