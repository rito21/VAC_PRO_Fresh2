from datetime import datetime

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.backend.database import Base


class Device(Base):
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True, index=True)
    alias = Column(String, nullable=False)
    description = Column(String)
    latitude = Column(Float, nullable=False)
    length = Column(Float, nullable=False)
    deveui = Column(String, unique=True, nullable=False)
    register_date = Column(DateTime, default=datetime.now, nullable=False)
    favourite = Column(Boolean, default=False)
    f_date = Column(DateTime)
    unregister = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    user_owner = Column(Integer, ForeignKey('app_user.user_id'), nullable=False)

    user = relationship("User", back_populates="devices")