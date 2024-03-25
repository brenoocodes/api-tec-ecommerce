from fastapi import HTTPException, status, Depends, Response
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from src.configure import SECRET_KEY, ALGORITHM, db_dependency
from typing import Annotated
from src.models.models import Clientes

ouauth2_bearer = OAuth2PasswordBearer(tokenUrl='/login')

def criar_token_acesso(email: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': email, 'id': user_id,}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM) 

def verificar_login(db: db_dependency, response: Response, token: Annotated[str, Depends(ouauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Usuário inválido')
        
        cliente = db.query(Clientes).filter(Clientes.id == user_id).first()
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cliente não existe')
        if not cliente.ativo:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Esse cliente foi desativado')

        return {'username': username, 'id': user_id}  

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token não é mais válido')


logado = Annotated[dict, Depends(verificar_login)]



