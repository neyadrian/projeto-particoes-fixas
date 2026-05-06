from models.processo import Processo
from models.particao import Particao

class SistemaMemoria:
    def __init__(self, tamanhos_particoes):
        self.particoes = []
        self.fila_espera = []
        self.ciclo_atual = 0
        self.total_fila = 0        
        self.tempos_espera = []    

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
        self.total_fila += 1
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
                        self.tempos_espera.append(processo_fila.ciclo_alocado - processo_fila.ciclo_chegada)
                        self.fila_espera.remove(processo_fila)
                        print(f"[Ciclo {self.ciclo_atual}] Processo {processo_fila.id} saiu da fila -> Partição {particao.id}")
                        return True
                return True

        print(f"[Ciclo {self.ciclo_atual}] Processo {id_processo} não encontrado")
        return False
    
    def relatorio(self):
        print("\n========== RELATÓRIO FINAL ==========")

        print(f"Processos que entraram na fila: {self.total_fila}")

        if self.tempos_espera:
            media_espera = sum(self.tempos_espera) / len(self.tempos_espera)
        else:
            media_espera = 0
        print(f"Tempo médio de espera: {media_espera:.2f} ciclos")

        utilizacoes = []
        for p in self.particoes:
            if not p.esta_livre():
                utilizacoes.append(p.processo.tamanho / p.tamanho * 100)
        media_util = sum(utilizacoes) / len(utilizacoes) if utilizacoes else 0
        print(f"Utilização média das partições: {media_util:.2f}%")

        memoria_total = sum(p.tamanho for p in self.particoes)
        frag_interna = sum(
            p.tamanho - p.processo.tamanho
            for p in self.particoes
            if not p.esta_livre()
        )
        print(f"Fragmentação interna total: {frag_interna / memoria_total * 100:.2f}%")
        print("=====================================\n")