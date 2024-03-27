import sys
from pathlib import Path
file = Path(__file__).resolve()
parent = file.parent.parent.parent
sys.path.append(str(parent))

from sqlalchemy import Boolean, Column, Integer, Float, String, ForeignKey, DateTime, JSON
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

    entradas = relationship('Entradas', backref='funcionario', lazy=True, foreign_keys='Entradas.funcionario_responsavel_matricula')

class Clientes(Base):
    __tablename__ = 'clientes'
    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True, nullable=False)
    cpf = Column(String(20), unique=True, nullable=False)
    data_de_nascimento = Column(String(20))
    nome = Column(String(120), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    senha = Column(String(100), nullable=False)
    email_confirmado = Column(Boolean, default=False)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    data_atualizacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    email_token = relationship('EmailToken', backref='cliente', lazy=True, foreign_keys='EmailToken.cliente_id')
    enderecos = relationship('Enderecos', backref='cliente', lazy=True, foreign_keys='Enderecos.cliente_id')
    compras = relationship('Vendas', backref='cliente', lazy=True, foreign_keys='Vendas.cliente_id')

class Enderecos(Base):
    __tablename__ = 'enderecos'
    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True, nullable=False)
    cliente_id = Column(String(36), ForeignKey('clientes.id'), nullable=False)
    cep = Column(String(10), nullable=False)
    cidade = Column(String(200), nullable=False)
    estado = Column(String(100), nullable=False)
    logradouro = Column(String(250), nullable=False)
    bairro = Column(String(250), nullable=False)
    numero = Column(String(20), nullable=True) #Aqui a gente pode colocar 2B, ou etc
    referencia = Column(String(150), nullable=True)
    observacao = Column(String(200), nullable=True)
    data_criacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    data_atualizacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    vendas = relationship('Vendas', backref='endereco', lazy=True, foreign_keys='Vendas.endereco_id')


class Categorias(Base):
    __tablename__ = 'categorias'
    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True, nullable=False)
    nome = Column(String(50), unique=True, nullable=False)
    data_criacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    data_atualizacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    produtos = relationship('Produtos', backref='categoria', lazy=True, foreign_keys='Produtos.categoria_id')

class Fornecedores(Base):
    __tablename__ = 'fornecedores'
    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True, nullable=False)
    cnpj = Column(String(14), unique=True, nullable=False)
    razao_social = Column(String(255), nullable=False)
    nome_fantasia = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    telefone = Column(String(14), nullable=False)
    data_criacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    data_atualizacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    entradas = relationship('Entradas', backref='fornecedor', lazy=True, foreign_keys='Entradas.fornecedor_id')

class Produtos(Base):
    __tablename__ = 'produtos'
    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True, nullable=False)
    categoria_id = Column(String(36), ForeignKey('categorias.id'), nullable=False)
    nome = Column(String(120), nullable=False)
    nome_estoque = Column(String(120), nullable=False)
    descricao = Column(JSON, nullable=True, default={})
    data_criacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    data_atualizacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    fornecedores = relationship('Fornecedores', secondary='produtos_fornecedores', backref=backref('produtos', lazy='dynamic'))

    itensestoque = relationship('ItensEstoque', backref='produtos', lazy=True, foreign_keys='produto_id')
    entradas = relationship('Entradas', backref='produto', lazy=True, foreign_keys='Entradas.produto_id')

class ProdutosFornecedores(Base):
    __tablename__ = 'produtos_fornecedores'
    produto_id = Column(Integer, ForeignKey('produtos.id'), primary_key=True)
    fornecedor_id = Column(Integer, ForeignKey('fornecedores.id'), primary_key=True)

class ItensEstoque(Base):
    __tablename__ = 'itensestoque'
    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True, nullable=False)
    produto_id = Column(String(36), ForeignKey('produtos.id'), nullable=False)
    preco = Column(Float, default=0, nullable=False)
    cor = Column(String(50), nullable=False)
    quantidade = Column(Integer, default=0)
    imagens = Column(JSON, nullable=True, default={})
    

    itenscarrinho = relationship('ItensCarrinhos', backref='itemestoque', lazy=True, foreign_keys='ItensCarrinhos.itemestoque_id')
    itemvendas = relationship('ItensVendas', backref='itemestoque', lazy=True, foreign_keys='ItensVendas.itemestoque_id')

class Entradas(Base):
    __tablename__ = 'entradaestoque'
    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True, nullable=False)
    nota = Column(String(50), nullable=False)
    produto_id = Column(String(36), ForeignKey('itensestoque.id'), nullable=False)
    fornecedor_id = Column(String(36), ForeignKey('fornecedores.id'), nullable=False)
    data_criacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    data_atualizacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    quantidade = Column(Integer, nullable=False)
    funcionario_responsavel_matricula = Column(Integer, ForeignKey('funcionarios.matricula'), nullable=False)


class Carrinhos(Base):
    __tablename__ = 'carrinhos'
    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True, nullable=False)
    nome = Column(String(150), nullable=False)
    descricao = Column(String(250), nullable=True)
    quantidade_itens = Column(Integer, nullable=True)
    valor_total = Column(Float, nullable=True)
    data_criacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    data_atualizacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    itens = relationship('ItensCarrinhos', backref='carrinho', lazy=True, foreign_keys='ItensCarrinhos.carrinho_id')
    vendas = relationship('Vendas', backref='carrinho', lazy=True, foreign_keys='Vendas.carrinho_id')


class ItensCarrinhos(Base):
    __tablename__ = 'itenscarrinhos'
    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True, nullable=False)
    carrinho_id = Column(String(36), ForeignKey('carrinhos.id'), nullable=False)
    itemestoque_id = Column(String(36), ForeignKey('itensestoque.id'), nullable=False)
    valor_unitario = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)


class Vendas(Base):
    __tablename__ = 'vendas'
    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True, nullable=False)
    cliente_id = Column(String(36), ForeignKey('clientes.id'), nullable=False) 
    endereco_id = Column(String(36), ForeignKey('enderecos.id'), nullable=False)
    carrinho_id = Column(String(36), ForeignKey('carrinhos.id'), nullable=True)
    status = Column(String(50), nullable=False)
    link_pagamento = Column(String(200), nullable=True)
    pagamento_confirmado = Column(Boolean, default=False)
    data_criacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    data_atualizacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    itensvendas = relationship('ItensVendas', backref='venda', lazy=True, foreign_keys='ItensVendas.venda_id')


class ItensVendas(Base):
    __tablename__ = 'itensvendas'
    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True, nullable=False)
    venda_id = Column(String(36), ForeignKey('vendas.id'), nullable=False)
    itemestoque_id = Column(String(36), ForeignKey('itensestoque.id'), nullable=False)
    valor_unitario = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)


class EmailToken(Base):
    __tablename__ = 'emailtoken'
    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True, nullable=False)
    cliente_id = Column(String(36), ForeignKey('clientes.id'), nullable=False)
    email = Column(String(50), nullable=False)
    token = Column(String(200), nullable=False)
    data_criacao = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))



# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)