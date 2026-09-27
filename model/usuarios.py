from sqlalchemy import Column, String, Integer
from model.base import Base
from sqlalchemy.orm import relationship

class Usuarios(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String(140), unique=True, nullable=False)
    cpf = Column(String(11)) #não foi inserido "Unique" nesta coluna, pois o mesmo CPF pode ter várias contas
    email = Column(String(60), unique=True)

    def __init__ (self, nome:str, cpf:str, email:str):
        self.nome = nome
        self.cpf = cpf
        self.email = email
    
    #construindo a relação com a tabela Lista
    lista = relationship("Lista")


