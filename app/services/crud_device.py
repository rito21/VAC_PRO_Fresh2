from sqlalchemy.orm import Session
from starlette import status
from fastapi import HTTPException
from app.models.device import Device
from app.schemas.device import DeviceCreate


def create_device(db: Session, device: DeviceCreate):
    db_device = Device(**device.model_dump())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return status.HTTP_201_CREATED


def get_all_devices_for_user(db: Session, user_id: int):
    return db.query(Device).filter_by(user_owner=user_id, unregister=False)


def get_device_by_id(db: Session, device_id: int):
    return db.query(Device).filter_by(id=device_id).first()


def get_devices_favourites(db: Session, user_id: int):
    return db.query(Device).filter_by(user_owner=user_id, unregister=False, favourite=True)


def delete_device_by_id(db: Session, device_id: int):
    device = get_device_by_id(db, device_id)

    if device is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aparell no trobat")

    device.unregister = True
    db.commit()
    db.refresh(device)
    return status.HTTP_200_OK


def set_device_favourite(db: Session, device_id: int):
    device = get_device_by_id(db, device_id)

    if device is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aparell no trobat")

    device.favourite = not device.favourite
    db.commit()
    db.refresh(device)
    return status.HTTP_200_OK