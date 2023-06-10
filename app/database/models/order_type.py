import json
import uuid
from sqlalchemy import Column, DateTime, String
from app.database.base import Base
from sqlalchemy.sql import func

class OrderType(Base):

    __tablename__ = "order_types"

    id          = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    Name        = Column(String(128))
    Description = Column(String(64))
    CreatedAt   = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt   = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, id, Name, Description):
        super().__init__()
        self.id          = id
        self.Name        = Name
        self.Description = Description

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr
