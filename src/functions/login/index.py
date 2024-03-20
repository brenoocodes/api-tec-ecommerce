from fastapi import status, Depends, Response
from pydantic import BaseModel
from datetime import timedelta
from src.configure import db_dependency, router, app
from src.models.models import Clientes
from typing import Annotated
from src.functions.login.senha import *
from src.functions.login.token import verificar_login, criar_token_acesso


class Login(BaseModel):
    username: str
    password: str

@router.post("/login", status_code=200)
async def login(Login: Login, db: db_dependency, response: Response):
    try:
        cliente_existente = db.query(Clientes).filter(Clientes.email == Login.username).first()
        if not cliente_existente:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'mensagem': 'Cliente ainda não cadastrado'}
        if verificar_senha(Login.password, cliente_existente.senha) == True:
            token = criar_token_acesso(cliente_existente.email, cliente_existente.id, timedelta(days=30))
            resposta = {
                'token': token,
                'cliente_id': cliente_existente.id,
                'cliente_nome': cliente_existente.nome,
                'cliente_email': cliente_existente.email
            }
            return {'mensagem': 'Cliente logado com sucesso', 'data': resposta}
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'mensagem': 'Senha incorreta'}

    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'Erro de servidor {e}'}
    
    
logado = Annotated[dict, Depends(verificar_login)]

app.include_router(router)

