from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from app.database import get_db
from app.models import Usuari
from app.auth import authenticate_user, create_access_token
from fastapi import BackgroundTasks

router = APIRouter()



def log_login(correu_electronic: str):
    import time
    time.sleep(3)
    print(f"Inicio de sesión registrado para {correu_electronic}")

@router.post("/login/")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.correu_electronic})
    if background_tasks:
        background_tasks.add_task(log_login, user.correu_electronic)

    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user():
    return None