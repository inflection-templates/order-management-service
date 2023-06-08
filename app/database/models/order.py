import json
import uuid
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database.connector import Base


class Order(Base):

    __tablename__ = "orders"

    id = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    displayCode = Column(String(36), unique=True, index=True)
    invoiceNumber = Column(String(64), unique=True, index=True)
    customerCartId = Column(String(36), default=None)
    TotalItemsCount = Column(Integer, default=0)
    OrderDiscount = Column(Float, default=0.0)
    TipApplicable = Column(Boolean, default=False)
    TipAmount = Column(Float, default=0.0)
    TotalTax = Column(Float, default=0.0)
    TotalDiscount = Column(Float, default=0.0)
    TotalAmount = Column(Float, default=0.0)
    Notes = Column(String(1024), default=None)
    Customer = relationship("Customer", back_populates="orders", default=None)
    OrderLineItems = relationship("OrderLineItem", back_populates="Order", default=None)
    Coupon = relationship("Coupon", back_populates="order", default=None)
    PaymentTransactionId = Column(String(36), ForeignKey("transactions.id"), default=None)
    RefundTransactionId = Column(String(36), ForeignKey("transactions.id"), default=None)
    OrderStatus = Column(String(36), ForeignKey("order_statuses.id"), default=None)
    OrderType = Column(String(36), ForeignKey("order_types.id"), default=None)

    def __init__(self, id, displayCode, invoiceNumber, customerCartId, TotalItemsCount, OrderDiscount, TipApplicable, TipAmount, TotalTax, TotalAmount, TotalDiscount, Notes):
        super().__init__()
        self.id = id
        self.displayCode = displayCode
        self.invoiceNumber = invoiceNumber
        self.customerCartId = customerCartId
        self.TotalItemsCount = TotalItemsCount
        self.OrderDiscount = OrderDiscount
        self.TipApplicable = TipApplicable
        self.TipAmount = TipAmount
        self.TotalTax = TotalTax
        self.TotalDiscount = TotalDiscount
        self.TotalAmount = TotalAmount
        self.Notes = Notes

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr