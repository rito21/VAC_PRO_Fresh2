from fastapi import FastAPI, Depends, HTTPException, status, Request, Response, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.staticfiles import StaticFiles
from app.database import get_db, init_db
from app.models import Usuari, Empresa, Device
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.auth import get_password_hash, authenticate_user
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import jwt
from jose import JWTError

# Inicializar la aplicación FastAPI
app = FastAPI()

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar plantillas
templates = Jinja2Templates(directory="templates")

# Inicializar la base de datos
try:
    init_db()
    print("Base de datos inicializada correctamente")
except Exception as e:
    print(f"Error al inicializar la base de datos: {e}")
    raise

def create_default_empresa(db: Session):
    empresa = db.query(Empresa).first()
    if not empresa:
        new_empresa = Empresa(nom_empresa="Default Empresa")
        db.add(new_empresa)
        db.commit()
        db.refresh(new_empresa)
    return db.query(Empresa).first()

# Configuración para JWT (sincronizada con app/auth.py)
SECRET_KEY = "8fe87ab237c9f1f87f985078c1aef58c17aca40f68c649d029e9c3bcefe67f83"
ALGORITHM = "HS256"

# Configurar HTTPBearer para manejar cabeceras Authorization
security = HTTPBearer(auto_error=False)


async def get_token(
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Para depuración
    print(f"Cookies recibidas: {request.cookies}")
    if credentials:
        print(f"Header Authorization: {credentials.credentials}")

    # Intentar obtener el token de la cookie
    token = request.cookies.get("token")
    if token:
        # No quitar el prefijo "Bearer" si la validación espera el prefijo completo
        print(f"Token extraído de cookie: {token}")
        return token

    # Si no hay token en la cookie, intentar obtenerlo de la cabecera
    if credentials:
        print(f"Token extraído de header: {credentials.credentials}")
        return credentials.credentials

    print("No se encontró token")
    return None


async def get_current_user(
        token: str = Depends(get_token),
        db: Session = Depends(get_db)
) -> Optional[Usuari]:
    if not token:
        return None

    # Si el token tiene el prefijo "Bearer", quitarlo antes de decodificar
    if token.startswith("Bearer "):
        token = token[7:]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correu_electronic: str = payload.get("sub")
        if not correu_electronic:
            return None
    except Exception as e:
        print(f"Error decodificando token: {e}")
        return None

    user = db.query(Usuari).filter(Usuari.correu_electronic == correu_electronic).first()
    return user

# Rutas
@app.post("/signup/")
async def signup(
    correu_electronic: str = Form(...),
    contrasenya: str = Form(...),
    confirmar_contrasenya: str = Form(...),
    nom: str = Form(...),
    cognoms: str = Form(...),
    db: Session = Depends(get_db)
):
    if contrasenya != confirmar_contrasenya:
        raise HTTPException(status_code=400, detail="Les contrasenyes no coincideixen")
    db_user = db.query(Usuari).filter(Usuari.correu_electronic == correu_electronic).first()
    if db_user:
        raise HTTPException(status_code=400, detail="L'email ja està registrat")
    empresa = create_default_empresa(db)
    hashed_password = get_password_hash(contrasenya)
    print(f"Registrando usuario - Correu: {correu_electronic}, Hash: {hashed_password}")
    new_user = Usuari(
        id_empresa=empresa.id,
        correu_electronic=correu_electronic,
        contrasenya=hashed_password,
        nom=nom,
        cognoms=cognoms
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return RedirectResponse(url="/login/", status_code=302)


@app.get("/debug-auth/")
async def debug_auth(request: Request):
    token = request.cookies.get("token")
    headers = dict(request.headers)
    auth_header = headers.get("authorization")

    result = {
        "has_cookie": token is not None,
        "cookie_value": token[:15] + "..." if token else None,
        "has_auth_header": auth_header is not None,
        "auth_header_value": auth_header[:15] + "..." if auth_header else None
    }

    if token:
        try:
            if token.startswith("Bearer "):
                pure_token = token[7:]
            else:
                pure_token = token

            payload = jwt.decode(pure_token, SECRET_KEY, algorithms=[ALGORITHM])
            result["token_valid"] = True
            result["payload"] = payload
        except Exception as e:
            result["token_valid"] = False
            result["error"] = str(e)

    return result
@app.get("/test-token/")
async def test_token(token: str = Depends(get_token)):
    if not token:
        return {"valid": False, "error": "No token provided"}
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"valid": True, "payload": payload}
    except Exception as e:
        return {"valid": False, "error": str(e)}


@app.get("/login/", response_class=HTMLResponse)
async def login_form(request: Request, current_user: Optional[Usuari] = Depends(get_current_user)):
    return templates.TemplateResponse("login.html", {"request": request, "lang": "ca", "current_user": current_user})

@app.get("/protected/", response_class=HTMLResponse)
async def protected_route_html(request: Request, current_user: Usuari = Depends(get_current_user)):
    if not current_user:
        print(f"Redirigiendo a /login/ desde {request.url.path} por falta de autenticación")
        return RedirectResponse(url="/login/", status_code=302)
    return templates.TemplateResponse("protected.html", {"request": request, "lang": "ca", "current_user": current_user})

@app.get("/api/protected/")
async def protected_api(current_user: Usuari = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="No autenticado")
    return {"message": f"Benvingut, {current_user.nom} {current_user.cognoms}! Aquesta és una àrea protegida."}

@app.get("/devices/", response_class=HTMLResponse)
async def list_devices(request: Request, current_user: Usuari = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user:
        return RedirectResponse(url="/login/", status_code=302)
    devices = db.query(Device).filter(Device.id_usuari == current_user.id).all()
    return templates.TemplateResponse("devices.html", {"request": request, "lang": "ca", "current_user": current_user, "devices": devices})

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, current_user: Optional[Usuari] = Depends(get_current_user)):
    return templates.TemplateResponse("home.html", {"request": request, "lang": "ca", "current_user": current_user})

# Incluir routers adicionales
app.include_router(auth_router)
app.include_router(users_router)