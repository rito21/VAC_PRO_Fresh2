from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from app.backend.database import Base
from app.models.company import Company
from app.models.device import Device


class User(Base):
    __tablename__ = 'app_user'

    email = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, primary_key=True, index=True)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    creation_date = Column(DateTime, default=datetime.utcnow)
    company_id = Column(Integer, ForeignKey('company.id'), nullable=False)
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    last_access_date = Column(DateTime, default=datetime.utcnow)
    is_locked = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

    company_rel = relationship("Company", back_populates="users")
    devices = relationship("Device", back_populates="user")