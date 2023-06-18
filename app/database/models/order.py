import json
import uuid
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, func, Enum as EnumColumn
from sqlalchemy.orm import relationship
from app.common.utils import generate_uuid4
from app.database.base import Base
from app.domain_types.enums.order_status_types import OrderStatusTypes


class Order(Base):

    __tablename__ = "orders"

    id                   = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
    DisplayCode          = Column(String(36), unique=True, index=True)
    OrderStatus          = Column(EnumColumn(OrderStatusTypes), default=OrderStatusTypes.DRAFT.value)
    InvoiceNumber        = Column(String(64), unique=True, index=True)
    AssociatedCartId     = Column(String(36), ForeignKey("carts.id"), default=None)
    TotalItemsCount      = Column(Integer, default=0)
    OrderDiscount        = Column(Float, default=0.0)
    TipApplicable        = Column(Boolean, default=False)
    TipAmount            = Column(Float, default=0.0)
    TotalTax             = Column(Float, default=0.0)
    TotalDiscount        = Column(Float, default=0.0)
    TotalAmount          = Column(Float, default=0.0)
    Notes                = Column(String(1024), default=None)
    CustomerId           = Column(String(36), ForeignKey("customers.id"), default=None)
    PaymentTransactionId = Column(String(36), ForeignKey("payment_transactions.id"), default=None)
    RefundTransactionId  = Column(String(36), ForeignKey("payment_transactions.id"), default=None)
    ShippingAddressId    = Column(String(36), ForeignKey("addresses.id"), default=None)
    BillingAddressId     = Column(String(36), ForeignKey("addresses.id"), default=None)
    OrderType            = Column(String(36), ForeignKey("order_types.id"), default=None)
    CreatedAt            = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt            = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr
