import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, APIRouter
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from typing import Annotated

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'

app = FastAPI()

router = APIRouter()

SQL = os.getenv('SQL')
engine = create_engine(SQL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Corrigindo para chamar a função close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/")
def home():
    return {'Olá': 'Mundo'}

app.include_router(router)