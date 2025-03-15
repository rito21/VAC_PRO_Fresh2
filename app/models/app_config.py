from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from app.backend.database import Base


class AppConfig(Base):
    __tablename__ = 'app_config'

    id = Column(Integer, primary_key=True, index=True)
    passwd_length = Column(Integer, default=10)
    max_tries = Column(Integer, default=6)
    passwd_exp = Column(Integer, default=12)

    company = relationship("Company", back_populates="app_config")