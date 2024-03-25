from pydantic import BaseModel, EmailStr
from typing import Optional

class Clientes(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    cpf: str