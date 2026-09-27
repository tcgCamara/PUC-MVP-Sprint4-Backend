from pydantic import BaseModel
from model.lista import Lista

class AdicionarListaSchema (BaseModel):
    """Formato para adicionar as cartas na lista do usuario
    """
    usuario:str
    carta:str 
    quantidade:int

class RetornoListaSchema (BaseModel):
    """Retorna para o Front os dados estruturados após a inserção no banco de dados.
    """
    usuario_id:int
    carta:str 
    quantidade:int

class DeletarCartasSchema (BaseModel):
    """Modelo para apagar todas as cartas de mesmo título no banco.
    """
    usuario:str
    carta:str

class DeletarTodasAsCartasDoUsuario (BaseModel):
    """Modelo para apagar todas as cartas de mesmo título no banco.
    """
    usuario:str

class CodigoPostalFormato (BaseModel):
    """Define o modelo de entrada de dados
    """
    cep: str

class RetornoCepDoCliente (BaseModel):
    """Estrutura para retornar as informações da API externa referente ao CEP buscado
    """
    bairro:str
    cep: str
    estado: str
    estadouf: str
    cidade: str
    rua: str



def estrutura_lista (carta: Lista, usuario:str):
   return {
        "usuario": usuario,
        "carta": carta.carta,
        "quantidade": carta.quantidade
    }

def estrutura_cep (dadosJSON):
    return {
        'bairro': dadosJSON['bairro'],
        'cep': dadosJSON['cep'],
        'estado': dadosJSON['estado'],
        'estadouf': dadosJSON['uf'],
        'cidade': dadosJSON['localidade'],
        'rua': dadosJSON['logradouro']
    }

