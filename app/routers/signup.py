from fastapi import APIRouter, Request, Form, Depends, Response
from sqlalchemy.orm import Session

from app.auth.login import is_valid_password, create_access_token
from app.backend.database import get_db
from app.schemas.user import UserCreate

from app.services.crud_user import get_user_by_email, create_user

router = APIRouter(tags=['signup'])


@router.post("/signup")
def signup(request: Request,
           email: str = Form(...),
           password: str = Form(...),
           name: str = Form(...),
           db: Session = Depends(get_db)):
    # Verificar si l'usuari ja existeix
    db_user = get_user_by_email(db, email)
    if db_user:
        return [Response("Correu electrònic ja registrat", status_code=404)]

    # Validar la força de la contrasenya
    if not is_valid_password(password):
        return [Response("La contrasenya no compleix els requisits de seguretat", status_code=404)]

    new_user = UserCreate(
        email=email,
        password=password,
        full_name=name,
        company_id=1,
    )
    user = create_user(db, new_user)

    create_access_token(user=user)

    return [Response("Usuari registrat correctament")]