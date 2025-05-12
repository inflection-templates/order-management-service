# import json
# import uuid
# from sqlalchemy import Column, DateTime, String
# from app.common.utils import generate_uuid4
# from app.database.base import Base
# from sqlalchemy.sql import func

# class OrderType(Base):

#     __tablename__ = "order_types"

#     id          = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
#     Name        = Column(String(128))
#     Description = Column(String(64))
#     CreatedAt   = Column(DateTime(timezone=True), server_default=func.now())
#     UpdatedAt   = Column(DateTime(timezone=True), onupdate=func.now())

#     def __init__(self, id, Name, Description):
#         super().__init__()
#         self.id          = id
#         self.Name        = Name
#         self.Description = Description

#     def __repr__(self):
#         jsonStr = json.dumps(self.__dict__)
#         return jsonStr


from sqlmodel import SQLModel, Field
from sqlalchemy.sql import func
from app.common.utils import generate_uuid4
from typing import Optional
from datetime import datetime

class OrderType(SQLModel, table=True):
    __tablename__ = "order_types"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    Name: str = Field(..., max_length=128)
    Description: Optional[str] = Field(default=None, max_length=64)
    CreatedAt: datetime = Field(default_factory=func.now, sa_column_kwargs={"timezone": True})
    UpdatedAt: datetime = Field(default_factory=func.now, sa_column_kwargs={"timezone": True}, sa_column_onupdate=func.now())

    def __repr__(self):
        return self.json(indent=2)
