from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime

from sqlalchemy.orm import relationship

from app.backend.database import Base
from app.models.app_config import AppConfig


class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    cif = Column(String, unique=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    active = Column(Boolean, default=True)
    app_config_id = Column(Integer, ForeignKey('app_config.id'))

    app_config = relationship("AppConfig", back_populates="company")
    users = relationship("User", back_populates="company_rel")