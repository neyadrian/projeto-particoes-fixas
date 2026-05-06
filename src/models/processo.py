from dataclasses import dataclass

@dataclass
class Processo:
    def __init__(self, id, tamanho, ciclo_chegada):
        self.id = id
        self.tamanho = tamanho
        self.ciclo_chegada = ciclo_chegada
        self.ciclo_alocado = None