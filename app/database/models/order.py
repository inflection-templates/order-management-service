import json
import uuid
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, func, Enum as EnumColumn
from sqlalchemy.orm import relationship
from app.database.database_accessor import Base
from app.domain_types.enums.order_status_types import OrderStatusTypes


class Order(Base):

    __tablename__ = "orders"

    id                   = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    DisplayCode          = Column(String(36), unique=True, index=True)
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
    Customer             = relationship("Customer", back_populates="orders", default=None)
    OrderLineItems       = relationship("OrderLineItem", back_populates="Order", default=None)
    Coupon               = relationship("Coupon", back_populates="order", default=None)
    PaymentTransactionId = Column(String(36), ForeignKey("transactions.id"), default=None)
    RefundTransactionId  = Column(String(36), ForeignKey("transactions.id"), default=None)
    OrderStatus          = Column(EnumColumn(OrderStatusTypes), default=OrderStatusTypes.DRAFT.value)
    OrderType            = Column(String(36), ForeignKey("order_types.id"), default=None)
    CreatedAt            = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt            = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, id, displayCode, invoiceNumber,
                 customerCartId = None, TotalItemsCount = 0, OrderDiscount = 0.0,
                 TipApplicable = False, TipAmount = 0.0, TotalTax = 0.0,
                 TotalAmount = 0.0, TotalDiscount = 0.0, Notes = None):
        super().__init__()
        self.id               = id
        self.DisplayCode      = displayCode
        self.InvoiceNumber    = invoiceNumber
        self.AssociatedCartId = customerCartId
        self.TotalItemsCount  = TotalItemsCount
        self.OrderDiscount    = OrderDiscount
        self.TipApplicable    = TipApplicable
        self.TipAmount        = TipAmount
        self.TotalTax         = TotalTax
        self.TotalAmount      = TotalAmount
        self.TotalDiscount    = TotalDiscount
        self.Notes            = Notes

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr
