from collections import OrderedDict
import json
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String, Enum as EnumColumn
from app.database.database_accessor import Base
from sqlalchemy.sql import func
from app.domain_types.enums.order_status_types import OrderStatusTypes

class OrderHistory(Base):

    __tablename__ = "order_histories"

    id              = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    OrderId         = Column(String(36), ForeignKey("orders.id"), default=None)
    PreviousStatus  = Column(EnumColumn(OrderStatusTypes), default=OrderStatusTypes.DRAFT.value)
    Status          = Column(EnumColumn(OrderStatusTypes), default=OrderStatusTypes.DRAFT.value)
    UpdatedByUserId = Column(String(36), default=None)
    Timestamp       = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, id, OrderId, Status, PreviousStatus, UpdatedByUserId = None):
        super().__init__()
        self.id              = id
        self.OrderId         = OrderId
        self.Status          = Status
        self.PreviousStatus  = PreviousStatus
        self.UpdatedByUserId = UpdatedByUserId

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr

