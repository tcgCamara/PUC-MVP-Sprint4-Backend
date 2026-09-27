from pydantic import BaseModel
from model.usuarios import Usuarios
from typing import Optional, List

class CadastroUsuario(BaseModel):
    """Cadastro do Usuário no back-end para login
    """
    nome: str = ""
    cpf: str = ""
    email: str = ""

class LoginUsuario (BaseModel):
    """Informa a estrutuda para realizar login.
    Esta informação é tratada pelo banco de dados.
    """
    nome: str

def estrutura_usuario (user: Usuarios):
    return {
        "nome": user.nome,
        "cpf": user.cpf,
        "email": user.email
    }

def estrutura_login (user: Usuarios):
    return {'nome': user.nome}


