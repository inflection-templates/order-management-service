import uuid
from app.common.utils import print_colorized_json
from app.database.database_accessor import DatabaseSession
from app.domain_types.order import OrderCreateModel, OrderResponseModel


def create_order(db_session: DatabaseSession, model: OrderCreateModel) -> OrderResponseModel:
    try:
        order = db_session.db.add(model)
        db_session.db.commit()
        db_session.db.refresh(model)
    except Exception as e:
        print(e)
        db_session.db.rollback()
        raise e
    finally:
        db_session.db.close()

    # order = OrderResponseModel(**model.dict(), id=uuid.uuid4(), DisplayCode="1234", InvoiceNumber="1234")
    print_colorized_json(order)
    return order

