from enum import Enum
import json
import uuid
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Float, Enum as EnumColumn
from sqlalchemy.orm import relationship
from app.database.connector import Base
from sqlalchemy.sql import func
from app.domain_types.order_status_types import OrderStatusTypes

class OrderStatus(Base):

    __tablename__ = "order_statuses"

    id = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    Status = Column(EnumColumn(OrderStatusTypes), default=OrderStatusTypes.DRAFT.value)
    Description = Column(String(64))
    OrderId = Column(String(36), ForeignKey("orders.id"), default=None)

    def __init__(self, id, Status, Description):
        super().__init__()
        self.id = id
        self.Status = Status
        self.Description = Description

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr

