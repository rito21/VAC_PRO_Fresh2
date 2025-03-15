from pydantic_settings import BaseSettings
from urllib import parse
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    # PostgreSQL
    DB_NAME: str = os.getenv('DB_NAME')
    DB_USER: str = os.getenv('DB_USER')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = os.getenv('DB_PORT')
    DB_SSL_MODE: str = 'require'

    # Token
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_SECONDS: int = os.getenv('ACCESS_TOKEN_EXPIRE_SECONDS')
    ALGORITHM: str = os.getenv('ALGORITHM')


settings = Settings()

# SQL Alchemy
settings.DB_PASSWORD = parse.quote_plus(settings.DB_PASSWORD)
SQLALCHEMY_DATABASE_URI: str = f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?sslmode={settings.DB_SSL_MODE}"
# Token
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_SECONDS = settings.ACCESS_TOKEN_EXPIRE_SECONDS
COOKIE_NAME = 'access_token'