from datetime import datetime

from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str
    cif: str
    app_config_id: int


class CompanyInfo(BaseModel):
    id: int
    name: str
    cif: str
    created_at: datetime
    active: bool
    app_config_id: int