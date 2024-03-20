from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from src.configure import SECRET_KEY, ALGORITHM
from typing import Annotated

ouauth2_bearer = OAuth2PasswordBearer(tokenUrl='/login')

def criar_token_acesso(email: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': email, 'id': user_id,}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM) 

def verificar_login(token: Annotated[str, Depends(ouauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')

        
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Usuário inválido')
        return {'username': username, 'id': user_id,}  

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token não é mais válido')





