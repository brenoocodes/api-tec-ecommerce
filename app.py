import uvicorn
from src.routes.clientes.index import *
from src.functions.login.index import *
from src.functions.email.verificar.verificarmail import *
from src.functions.email.recuperar_senha.index import *

if __name__ == "__main__":
    uvicorn.run("src.configure:app", port=5000, reload=True)