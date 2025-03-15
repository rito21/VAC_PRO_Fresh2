from werkzeug.security import generate_password_hash
from http.client import HTTPException

from sqlalchemy.orm import Session
from starlette import status

from app.models.user import User
from app.schemas.user import UserCreate


def create_user(db: Session, user_schema: UserCreate):
        user_schema.password = generate_password_hash(user_schema.password)
        user = User(**user_schema.model_dump())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


def update_user(self, user_id: int, user_schema: UserCreate) -> User:
    user = self.db_session.query(User).filter(User.user_id == user_id).first()
    if user:
        for var, value in vars(user_schema).items():
            if value is not None:
                setattr(user, var, value)
        self.db_session.commit()
        return user
    else:
        return status.HTTP_404_NOT_FOUND


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()