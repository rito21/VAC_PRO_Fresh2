from sqlalchemy.orm import Session
from app.models import Usuari
from app.schemas import UserCreate, UserUpdate
from app.auth import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(Usuari).filter(Usuari.id == user_id).first()

def get_user_by_email(db: Session, correu_electronic: str):
    return db.query(Usuari).filter(Usuari.correu_electronic == correu_electronic).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuari).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.contrasenya)
    db_user = Usuari(
        correu_electronic=user.correu_electronic,
        contrasenya=hashed_password,
        nom=user.nom,
        cognoms=user.cognoms,
        id_empresa=1  # Ajusta según tu lógica
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(Usuari).filter(Usuari.id == user_id).first()
    if db_user:
        update_data = user.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(Usuari).filter(Usuari.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user