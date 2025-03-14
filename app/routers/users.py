from fastapi import APIRouter, Depends, HTTPException, status, Form, BackgroundTasks
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from app.database import get_db
from app.models import Usuari
from app.auth import authenticate_user, create_access_token

router = APIRouter()

def log_login(correu_electronic: str):
    import time
    time.sleep(3)
    print(f"Inicio de sesión registrado para {correu_electronic}")

@router.post("/login/")
async def login(
    correu_electronic: str = Form(...),
    contrasenya: str = Form(...),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    print(f"Intento de login - Correu: {correu_electronic}, Contrasenya: {contrasenya}")
    user = authenticate_user(db, correu_electronic, contrasenya)
    if not user:
        print(f"Autenticación fallida para {correu_electronic}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.correu_electronic})
    print(f"Login exitoso - Token generado: {access_token}")
    if background_tasks:
        background_tasks.add_task(log_login, user.correu_electronic)
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(
        key="token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=3600,
        path="/",
        samesite="lax"
    )
    return response

def get_current_user():
    return None