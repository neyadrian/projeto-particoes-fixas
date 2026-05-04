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
    particoes: list[Particao] = field(default_factory=list)
    fila_espera: deque[Processo] = field(default_factory=deque)
    historico: list[dict] = field(default_factory=list)
    ciclo_atual: int = 0
    _utilizacao_por_ciclo: list[float] = field(default_factory=list)
    _fragmentacao_acumulada: int = 0

    def alocar(self, processo: Processo) -> bool:
        for particao in self.particoes:
            if not particao.ocupada and particao.tamanho >= processo.tamanho:
                particao.ocupada = True
                particao.processo = processo
                processo.tempo_alocacao = self.ciclo_atual
                self.historico.append({
                    "ciclo": self.ciclo_atual,
                    "acao": "alocacao",
                    "processo_id": processo.id,
                    "particao_endereco": particao.endereco_inicial,
                })
                return True

        processo.tempo_chegada = self.ciclo_atual
        self.fila_espera.append(processo)
        self.historico.append({
            "ciclo": self.ciclo_atual,
            "acao": "fila",
            "processo_id": processo.id,
        })
        return False

    def liberar(self, id_processo: int) -> bool:
        for particao in self.particoes:
            if particao.ocupada and particao.processo and particao.processo.id == id_processo:
                particao.processo.tempo_liberacao = self.ciclo_atual
                self.historico.append({
                    "ciclo": self.ciclo_atual,
                    "acao": "liberacao",
                    "processo_id": id_processo,
                    "particao_endereco": particao.endereco_inicial,
                })
                particao.ocupada = False
                particao.processo = None
                self.tentar_alocar_fila(particao)
                return True
        return False

    def tentar_alocar_fila(self, particao: Particao) -> bool:
        for i, processo in enumerate(self.fila_espera):
            if particao.tamanho >= processo.tamanho:
                self.fila_espera.remove(processo)
                particao.ocupada = True
                particao.processo = processo
                processo.tempo_alocacao = self.ciclo_atual
                self.historico.append({
                    "ciclo": self.ciclo_atual,
                    "acao": "alocacao_fila",
                    "processo_id": processo.id,
                    "particao_endereco": particao.endereco_inicial,
                })
                return True
        return False

    def migrar_processo(self, id_processo: int, indice_particao: int) -> bool:
        nova_particao = self.particoes[indice_particao]
        particao_origem = None
        processo_alvo = None

        for particao in self.particoes:
            if particao.ocupada and particao.processo and particao.processo.id == id_processo:
                particao_origem = particao
                processo_alvo = particao.processo
                break

        if not particao_origem or not processo_alvo:
            print(f"  [ERRO] Processo P{id_processo} não encontrado em nenhuma partição.")
            return False

        if nova_particao.ocupada:
            print(f"  [ERRO] Partição destino (índice {indice_particao}) já está ocupada.")
            return False

        if nova_particao.tamanho < processo_alvo.tamanho:
            print(f"  [ERRO] Partição destino (tamanho {nova_particao.tamanho}) é menor que o processo (tamanho {processo_alvo.tamanho}).")
            return False

        nova_particao.ocupada = True
        nova_particao.processo = processo_alvo

        particao_origem.ocupada = False
        particao_origem.processo = None

        self.historico.append({
            "ciclo": self.ciclo_atual,
            "acao": "migracao",
            "processo_id": id_processo,
            "origem": particao_origem.endereco_inicial,
            "destino": nova_particao.endereco_inicial,
        })

        self.tentar_alocar_fila(particao_origem)
        return True

    def _registrar_estado_ciclo(self):
        ocupadas = [p for p in self.particoes if p.ocupada and p.processo]
        if self.particoes:
            utilizacao = sum(p.processo.tamanho / p.tamanho for p in ocupadas) / len(self.particoes)
        else:
            utilizacao = 0.0
        self._utilizacao_por_ciclo.append(utilizacao)

        fragmentacao_ciclo = sum(p.tamanho - p.processo.tamanho for p in ocupadas)
        self._fragmentacao_acumulada += fragmentacao_ciclo

    def relatorio(self):
        self._registrar_estado_ciclo()

        print(f"\n{'=' * 60}")
        print(f"  RELATÓRIO — Ciclo {self.ciclo_atual}")
        print(f"{'=' * 60}")

        print(f"\n  {'Partição':<12} {'Tamanho':<10} {'Processo':<12} {'Frag. Int.':<12} {'Endereços'}")
        print(f"  {'-' * 58}")

        for i, p in enumerate(self.particoes):
            if p.ocupada and p.processo:
                frag = p.tamanho - p.processo.tamanho
                proc_str = f"P{p.processo.id} ({p.processo.tamanho})"
                frag_str = f"{frag}"
            else:
                proc_str = "LIVRE"
                frag_str = "-"

            print(f"  {i:<12} {p.tamanho:<10} {proc_str:<12} {frag_str:<12} [{p.endereco_inicial}-{p.endereco_final}]")

        if self.fila_espera:
            fila_str = ", ".join(f"P{p.id}({p.tamanho})" for p in self.fila_espera)
            print(f"\n  Fila de espera: {fila_str}")
        else:
            print(f"\n  Fila de espera: vazia")

        print(f"{'=' * 60}")

    def calcular_metricas(self) -> dict:
        processos_alocados = set()
        for entry in self.historico:
            if entry["acao"] in ("alocacao", "alocacao_fila"):
                processos_alocados.add(entry["processo_id"])

        tempos_espera = []
        processos_vistos = set()
        for entry in self.historico:
            pid = entry["processo_id"]
            if pid in processos_vistos:
                continue

            if entry["acao"] == "alocacao":
                tempos_espera.append(0)
                processos_vistos.add(pid)
            elif entry["acao"] == "fila":
                for e2 in self.historico:
                    if e2["processo_id"] == pid and e2["acao"] == "alocacao_fila":
                        tempos_espera.append(e2["ciclo"] - entry["ciclo"])
                        processos_vistos.add(pid)
                        break

        tempo_medio_espera = sum(tempos_espera) / len(tempos_espera) if tempos_espera else 0.0

        utilizacao_media = (
            sum(self._utilizacao_por_ciclo) / len(self._utilizacao_por_ciclo)
            if self._utilizacao_por_ciclo
            else 0.0
        )

        return {
            "total_processos_fila": len(self.fila_espera),
            "tempo_medio_espera": round(tempo_medio_espera, 2),
            "utilizacao_media_por_ciclo": round(utilizacao_media, 4),
            "fragmentacao_interna_total_acumulada": self._fragmentacao_acumulada,
        }


def criar_particoes(tamanhos: list[int]) -> list[Particao]:
    particoes = []
    endereco = 0
    for t in tamanhos:
        particoes.append(Particao(tamanho=t, endereco_inicial=endereco, endereco_final=endereco + t - 1))
        endereco += t
    return particoes


def cenario_1():
    print("\n" + "#" * 60)
    print("  CENÁRIO 1 — Sequência Manual")
    print("#" * 60)

    sistema = SistemaMemoria(particoes=criar_particoes([100, 200, 300, 400]))

    sistema.ciclo_atual = 1
    sistema.alocar(Processo(id=1, tamanho=80, tempo_chegada=1))
    sistema.relatorio()

    sistema.ciclo_atual = 2
    sistema.alocar(Processo(id=2, tamanho=190, tempo_chegada=2))
    sistema.relatorio()

    sistema.ciclo_atual = 3
    sistema.alocar(Processo(id=3, tamanho=290, tempo_chegada=3))
    sistema.relatorio()

    sistema.ciclo_atual = 4
    sistema.alocar(Processo(id=4, tamanho=390, tempo_chegada=4))
    sistema.relatorio()

    sistema.ciclo_atual = 5
    sistema.alocar(Processo(id=5, tamanho=150, tempo_chegada=5))
    sistema.relatorio()

    sistema.ciclo_atual = 6
    sistema.alocar(Processo(id=6, tamanho=50, tempo_chegada=6))
    sistema.relatorio()

    sistema.ciclo_atual = 7
    sistema.liberar(1)
    sistema.relatorio()

    sistema.ciclo_atual = 8
    sistema.liberar(3)
    sistema.relatorio()

    sistema.ciclo_atual = 9
    sistema.migrar_processo(2, 2)
    sistema.relatorio()

    sistema.ciclo_atual = 10
    metricas = sistema.calcular_metricas()
    print(f"\n{'=' * 60}")
    print("  MÉTRICAS FINAIS — Cenário 1")
    print(f"{'=' * 60}")
    for k, v in metricas.items():
        print(f"  {k}: {v}")
    print(f"{'=' * 60}")


def simular_aleatorio(n_ciclos: int = 20, seed: int = 42):
    print("\n" + "#" * 60)
    print("  CENÁRIO 2 — Simulação Aleatória")
    print("#" * 60)

    random.seed(seed)

    sistema = SistemaMemoria(particoes=criar_particoes([100, 200, 300, 400]))
    proximo_id = 1

    for ciclo in range(1, n_ciclos + 1):
        sistema.ciclo_atual = ciclo

        processos_alocados = [
            p.processo for p in sistema.particoes if p.ocupada and p.processo
        ]

        if processos_alocados and random.random() < 0.4:
            proc = random.choice(processos_alocados)
            print(f"\n  [Ciclo {ciclo}] Liberando P{proc.id}")
            sistema.liberar(proc.id)
        else:
            tamanho = random.randint(50, 380)
            print(f"\n  [Ciclo {ciclo}] Alocando P{proximo_id} (tamanho={tamanho})")
            sistema.alocar(Processo(id=proximo_id, tamanho=tamanho, tempo_chegada=ciclo))
            proximo_id += 1

        if ciclo % 5 == 0:
            sistema.relatorio()

    metricas = sistema.calcular_metricas()
    print(f"\n{'=' * 60}")
    print("  MÉTRICAS FINAIS — Cenário 2")
    print(f"{'=' * 60}")
    for k, v in metricas.items():
        print(f"  {k}: {v}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    cenario_1()
    simular_aleatorio()
