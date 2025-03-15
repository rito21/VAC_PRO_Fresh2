from datetime import datetime

from pydantic import BaseModel


class DeviceCreate(BaseModel):
    alias: str
    description: str
    deveui: str
    latitude: float
    length: float
    user_owner: int


class DeviceInfo(BaseModel):
    id: int
    alias: str
    description: str
    deveui: str
    latitude: float
    length: float
    register_date: datetime
    favourite: bool
    f_date: datetime
    unregister: bool
    active: bool
    user_owner: int