from dataclasses import dataclass

@dataclass
class Processo:
    id: int
    tamanho: int
    tempo_chegada: int
    tempo_alocacao: int = -1
    tempo_liberacao: int = -1