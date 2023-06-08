import json
import uuid
from sqlalchemy import Column, DateTime, Integer, String, Float, Boolean, func
from sqlalchemy.orm import relationship

from app.database.connector import Base

class CouponType(Base):
    __tablename__ = "coupon_types"
    id = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    Code = Column(String(64), unique=True)
    Name = Column(String(64))
    Description = Column(String(64))
    Coupons = relationship("Coupon", back_populates="CouponType", default=None)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __init__(self, id, Name, Description):
        super().__init__()
        self.id = id
        self.Name = Name
        self.Description = Description

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr

