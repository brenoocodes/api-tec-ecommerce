from fastapi import status, Depends, Response
from sqlalchemy import desc
from datetime import datetime, timezone
from pydantic import BaseModel
from datetime import timedelta
from src.configure import db_dependency, router, app
from src.models.models import Clientes, EmailToken
from typing import Annotated
from src.functions.login.senha import *
from src.functions.login.token import verificar_login, criar_token_acesso
from src.functions.email.verificar.verificarmail import verificar_email

class Login(BaseModel):
    username: str
    password: str

@router.post("/login", status_code=200)
async def login(Login: Login, db: db_dependency, response: Response):
    try:
        if '@' in Login.username:
            cliente_existente = db.query(Clientes).filter(Clientes.email == Login.username).first()
        else:
            cliente_existente = db.query(Clientes).filter(Clientes.cpf == Login.username).first()   
        if not cliente_existente:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'mensagem': 'Cliente ainda não cadastrado'}
        if verificar_senha(Login.password, cliente_existente.senha) == True:
            if cliente_existente.email_confirmado == False:
                ultimo_token = db.query(EmailToken).filter(EmailToken.email == cliente_existente.email).order_by(desc(EmailToken.data_criacao)).first()
                print(ultimo_token.data_criacao)
                if ultimo_token:
                    tempo_decorrido = (datetime.now(timezone.utc) - ultimo_token.data_criacao.replace(tzinfo=timezone.utc)).total_seconds()
                    print(tempo_decorrido)
                    if tempo_decorrido < 180: 
                        return {'mensagem': f'Token enviado há {tempo_decorrido} segundos, aguarde três minutos para pedir um novo token'}
                    else:
                        await verificar_email(cliente_existente.email, db)
                        return {'mensagem': 'Cliente com email ainda não verificado, novo token enviado'}
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


