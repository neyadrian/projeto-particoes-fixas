from dataclasses import dataclass, field
from collections import deque
from typing import Optional
import random


@dataclass
class Processo:
    id: int
    tamanho: int
    tempo_chegada: int
    tempo_alocacao: int = -1
    tempo_liberacao: int = -1


@dataclass
class Particao:
    tamanho: int
    endereco_inicial: int
    endereco_final: int
    ocupada: bool = False
    processo: Optional[Processo] = None


@dataclass
class SistemaMemoria:
    def __init__(self, tamanhos_particoes):
        self.particoes = []
        self.fila_espera = []
        self.ciclo_atual = 0

        endereco = 0
        for i, tamanho in enumerate(tamanhos_particoes):
            self.particoes.append(Particao(i, tamanho, endereco))
            endereco += tamanho