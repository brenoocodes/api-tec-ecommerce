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
import uuid

class Funcionarios(Base):
    __tablename__ = 'funcionarios'
    matricula = Column(String(36), default=str(uuid.uuid4()), primary_key=True, nullable=False)
    nome = Column(String(200), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    senha = Column(String(100), nullable=False)
    administrador = Column(Boolean, default=False)
    data_criacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    data_atualizacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

class Clientes(Base):
    __tablename__ = 'clientes'
    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True, nullable=False)
    cpf = Column(String(20), unique=True, nullable=False)
    nome = Column(String(120), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    senha = Column(String(100), nullable=False)
    email_confirmado = Column(Boolean, default=False)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    data_atualizacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    email_token = relationship('EmailToken', backref='cliente_token', lazy=True, foreign_keys='EmailToken.cliente_id')


class Categorias(Base):
    __tablename__ = 'categorias'
    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True, nullable=False)
    nome = Column(String(50), unique=True, nullable=False)
    data_criacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    data_atualizacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    produtos = relationship('Produtos', backref='categoria', lazy=True)

class Produtos(Base):
    __tablename__ = 'produtos'
    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True, nullable=False)
    categoria_id = Column(String(36), ForeignKey('categorias.id'), nullable=False)
    nome = Column(String(120), nullable=False)
    nome_estoque = Column(String(120), nullable=False)
    
    data_criacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    data_atualizacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))


class EmailToken(Base):
    __tablename__ = 'emailtoken'
    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True, nullable=False)
    cliente_id = Column(String(36), ForeignKey('clientes.id'), nullable=False)
    email = Column(String(50), nullable=False)
    token = Column(String(200), nullable=False)
    data_criacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))



# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)