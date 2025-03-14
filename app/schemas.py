from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    correu_electronic: str
    contrasenya: str
    nom: str
    cognoms: str

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    nom: Optional[str] = None
    cognoms: Optional[str] = None

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    correu_electronic: str
    nom: str
    cognoms: str

    class Config:
        orm_mode = True