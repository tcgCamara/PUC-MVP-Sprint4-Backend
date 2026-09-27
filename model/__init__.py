from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

#importar os modelos definidos para a base de dados
from model.base import Base
from model.usuarios import Usuarios
from model.lista import Lista

#definindo os daminhos do destino e a URL para o banco de dados
db_path = "database/"
db_url = f'sqlite:///{db_path}/db.sqlite3'

#veriricando se existe a pasta/caminho para salvar o banco de dados
if not os.path.exists(db_path):
    os.makedirs(db_path)

#construindo o motor de conexão com o DB
engine = create_engine(db_url, echo=False)

Session = sessionmaker(bind=engine)

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)

