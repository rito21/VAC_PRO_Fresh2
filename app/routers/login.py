from fastapi import APIRouter, Request, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.login import verify_password, create_access_token
from app.backend.config import COOKIE_NAME, ACCESS_TOKEN_EXPIRE_SECONDS
from app.backend.database import get_db
from app.schemas.token import Token
from app.services.crud_user import get_user_by_email

router = APIRouter(tags=['login'])


@router.post("/login")
def login_for_access_token(request: Request,
                           db: Session = Depends(get_db),
                           form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        return {"message": "Correu electrònic o contrasenya incorrectes", "status_code": 404}

    access_token = create_access_token(user)
    return [Response("Usuari autenticat correctament", headers={"set-cookie": f"{COOKIE_NAME}={access_token}; Max-Age={ACCESS_TOKEN_EXPIRE_SECONDS}"})]