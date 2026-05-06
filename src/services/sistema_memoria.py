from src.models.particao import Particao

class SistemaMemoria:
    def __init__(self, tamanhos_particoes):
        self.particoes = []
        self.fila_espera = []
        self.ciclo_atual = 0

        endereco = 0
        for i, tamanho in enumerate(tamanhos_particoes):
            self.particoes.append(Particao(i, tamanho, endereco))
            endereco += tamanho

    def alocar(self, processo):
        self.ciclo_atual += 1

        for particao in self.particoes:
            if particao.esta_livre() and particao.tamanho >= processo.tamanho:
                particao.processo = processo
                processo.ciclo_alocado = self.ciclo_atual
                print(f"[Ciclo {self.ciclo_atual}] Processo {processo.id} ({processo.tamanho}u) -> Partição {particao.id} ({particao.tamanho}u)")
                return True
            
        processo.ciclo_chegada = self.ciclo_atual
        self.fila_espera.append(processo)
        print(f"[Ciclo {self.ciclo_atual}] Processo {processo.id} ({processo.tamanho}u) -> FILA DE ESPERA")
        return False
    
    def liberar(self, id_processo):
        self.ciclo_atual += 1

        for particao in self.particoes:
            if particao.processo and particao.processo.id == id_processo:
                print(f"[Ciclo {self.ciclo_atual}] Processo {id_processo} liberou Partição {particao.id}")
                particao.processo = None

                for processo_fila in self.fila_espera:
                    if particao.tamanho >= processo_fila.tamanho:
                        particao.processo = processo_fila
                        processo_fila.ciclo_alocado = self.ciclo_atual
                        self.fila_espera.remove(processo_fila)
                        print(f"[Ciclo {self.ciclo_atual}] Processo {processo_fila.id} saiu da fila -> Partição {particao.id}")
                        return True
                return True

        print(f"[Ciclo {self.ciclo_atual}] Processo {id_processo} não encontrado")
        return False