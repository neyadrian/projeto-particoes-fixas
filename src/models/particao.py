from dataclasses import dataclass
from typing import Optional
from src.models.processo import Processo

@dataclass
class Particao:
    tamanho: int
    endereco_inicial: int
    endereco_final: int
    ocupada: bool = False
    processo: Optional[Processo] = None