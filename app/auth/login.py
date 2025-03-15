from datetime import datetime, timezone, timedelta
from typing import Optional
import re
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from werkzeug.security import check_password_hash

from app.backend.config import ACCESS_TOKEN_EXPIRE_SECONDS, SECRET_KEY, ALGORITHM
from app.backend.database import get_db
from app.models.company import Company
from app.models.user import User
from app.services.crud_user import get_user_by_email

from jose import jwt, JWTError


def authenticate_user(email: str, password: str, db: Session):
    """
    Autentica un usuari basant-se en el seu correu electrònic i contrasenya.
     Paràmetres:
        email (str): El correu electrònic de l'usuari.
        password (str): La contrasenya de l'usuari.
        db (Session): L'objecte de sessió de la base de dades.
     Retorna:
        user: L'objecte d'usuari autenticat.
     Llença:
        HTTPException: Si no es troba l'usuari, el compte està bloquejat per intents d'inici de sessió excessius o la contrasenya és incorrecta.
    """
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuari no trobat")

    config_company = db.query(Company.app_config).filter(Company.id == user.company_id).first()
    print(config_company)
    if user.failed_login_attempts >= config_company.max_tries:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Compte bloquejat per intents excessius")
    if not verify_password(password, user.password):
        user.failed_login_attempts += 1
        db.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contrasenya incorrecta")
    user.failed_login_attempts = 0
    db.commit()
    return user


def verify_password(plain_password, hashed_password):
    """
    Verifica si una contrasenya en clar coincideix amb una contrasenya hashada donada.

    Paràmetres:
        plain_password (str): La contrasenya en clar a verificar.
        hashed_password (str): La contrasenya hashada per comparar.

    Retorna:
        bool: True si la contrasenya en clar coincideix amb la contrasenya hashada, False en cas contrari.
    """
    return check_password_hash(hashed_password, plain_password)


def is_valid_password(password: str):
    """
    Comprova si una contrasenya és vàlida basant-se en els següents criteris:

    Paràmetres:
        password (str): La contrasenya a validar.

    Retorna:
        bool: True si la contrasenya és vàlida, False en cas contrari.
    """
    if len(password) < 8:
        return False
    if not re.search('[0-9]', password):
        return False
    if not re.search("[a-zA-Z]", password):
        return False
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True


def create_access_token(user: User):
    try:
        expire = datetime.now(timezone.utc) + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
        payload = {
            "email": user.email,
            "username": user.full_name,
            "expire": expire.strftime("%Y-%m-%d %H:%M:%S")
        }
        return jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)
    except Exception as ex:
        print(str(ex))
        raise ex


def verify_token(token: str) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Optional[str] = payload.get("email")
        if email is None:
            return False
        return True
    except JWTError:
        return False


def get_current_user(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No s'han pogut validar les credencials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not verify_token(token):
        raise credentials_exception
    email = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("email")
    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user