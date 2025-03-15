from fastapi import FastAPI
from app.routers.login import router as login_router
from app.routers.signup import router as signup_router

app = FastAPI(
    title="APIAgroconnect",
    description="Agroconnect API",
)

app.include_router(login_router)
app.include_router(signup_router)