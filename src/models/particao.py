from dataclasses import dataclass
from typing import Optional
from src.models.processo import Processo

@dataclass
class Particao:
    def __init__(self, id, tamanho, endereco_inicio):
        self.id = id
        self.tamanho = tamanho
        self.endereco_inicio = endereco_inicio
        self.processo = None

    def esta_livre(self):
        return self.processo is None