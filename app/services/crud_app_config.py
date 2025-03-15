from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from starlette import status
from app.models.app_config import AppConfig
from app.schemas.app_config import ConfigCreate


def create_config(db: Session):
    db_config = AppConfig()
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return status.HTTP_201_CREATED


def get_config_by_id(db: Session, config_id: int):
    return db.query(AppConfig).filter(AppConfig.id == config_id).first()


def update_config(db: Session, config_id: int, config: ConfigCreate):
    db_config = get_config_by_id(db, config_id)
    if db_config is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuracio no trobada")

    for key, value in config.model_dump().items():
        setattr(db_config, key, value)
        db.commit()
        db.refresh(db_config)
    return status.HTTP_200_OK