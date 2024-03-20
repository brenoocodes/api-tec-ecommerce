from fastapi import status, Response
from fastapi.responses import JSONResponse
from src.configure import app, router, db_dependency
from src.models import models
from src.schemas.clientes.index import Clientes
from src.functions.login.senha import gerar_senha_criptografada
from src.functions.email.verificar.verificarmail import verificar_email

@router.post("/clientes", status_code=201)
async def criar_cliente(db: db_dependency, cliente: Clientes, response: Response):
    try:
        cliente_existente = db.query(models.Clientes).filter(models.Clientes.email == cliente.email).first()
        if cliente_existente:
            response.status_code = status.HTTP_406_NOT_ACCEPTABLE
            return {'mensagem': 'Cliente já cadastrado'}
        senha = gerar_senha_criptografada(cliente.senha)
        novo_cliente = models.Clientes(
            nome = cliente.nome,
            email = cliente.email,
            senha = senha
        )
        db.add(novo_cliente)
        db.commit()
        db.refresh(novo_cliente)
        
        # Chamar a função verificar_email para enviar o email de verificação
        await verificar_email(cliente.email, db)
        
        return {'mensagem': 'Novo funcionário cadastrado com sucesso e email enviado para a verificação'}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'Erro de servidor {e}'}


app.include_router(router)