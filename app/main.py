from fastapi import FastAPI, Depends, HTTPException, status, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.database import get_db, init_db
from app.models import Usuari, Empresa
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.auth import get_password_hash, get_current_user  # Importar get_current_user desde app.auth
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

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
        raise HTTPException(status_code=400, detail="Passwords do not match")
    db_user = db.query(Usuari).filter(Usuari.correu_electronic == correu_electronic).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    empresa = create_default_empresa(db)
    hashed_password = get_password_hash(contrasenya)
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
    return {"message": "User created successfully"}

app.include_router(auth_router)
app.include_router(users_router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/login/", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/protected/", response_class=HTMLResponse)
async def protected_route_html(request: Request):
    return templates.TemplateResponse("protected.html", {"request": request})

@app.get("/api/protected/")
async def protected_route_json(current_user: Usuari = Depends(get_current_user)):
    return {"message": f"Hello {current_user.nom} {current_user.cognoms}"}