import json
import uuid
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database.connector import Base
from sqlalchemy.sql import func

class OrderType(Base):

    __tablename__ = "order_types"

    id = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    Name = Column(String(128))
    Description = Column(String(64))

    def __init__(self, id, Name, Description):
        super().__init__()
        self.id = id
        self.Name = Name
        self.Description = Description

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr
