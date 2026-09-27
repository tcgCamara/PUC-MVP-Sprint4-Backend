from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from model import Base 

class Lista (Base):
    __tablename__ = 'lista'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    carta = Column(String(140))
    quantidade = Column(Integer)

    def __init__ (self, usuario_id:int, carta:str, quantidade:int):
        self.usuario_id = usuario_id
        self.carta = carta
        self.quantidade = quantidade
        
    # usuarios = relationship('Usuarios')
