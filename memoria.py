class Processo:
    def __init__(self, id, tamanho, ciclo_chegada):
        self.id = id
        self.tamanho = tamanho
        self.ciclo_chegada = ciclo_chegada
        self.ciclo_alocado = None


class Particao:
    def __init__(self, id, tamanho, endereco_inicio):
        self.id = id
        self.tamanho = tamanho
        self.endereco_inicio = endereco_inicio
        self.processo = None

    def esta_livre(self):
        return self.processo is None


class SistemaMemoria:
    def __init__(self, tamanhos_particoes):
        self.particoes = []
        self.fila_espera = []
        self.ciclo_atual = 0

        endereco = 0
        for i, tamanho in enumerate(tamanhos_particoes):
            self.particoes.append(Particao(i, tamanho, endereco))
            endereco += tamanho