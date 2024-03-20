import sys
from pathlib import Path
# Obtém o diretório do arquivo atual e seu diretório pai
file = Path(__file__).resolve()
parent = file.parent.parent.parent
# Adiciona o diretório pai ao sys.path
sys.path.append(str(parent))

from sqlalchemy import Boolean, Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from src.configure import Base, engine
from datetime import datetime, timezone

class Clientes(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, unique=True, primary_key=True, nullable=False)
    nome = Column(String(120), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    senha = Column(String(100), nullable=False)
    data_criacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

class EmailToken(Base):
    __tablename__ = 'emailtoken'
    id = Column(Integer, unique=True, primary_key=True, nullable=False)
    token = Column(String(200), nullable=False)
    data_criacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)