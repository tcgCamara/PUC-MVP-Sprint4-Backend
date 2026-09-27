from pydantic import BaseModel
from typing import Optional, List

class ErroSchema(BaseModel):
    mensagem:str
