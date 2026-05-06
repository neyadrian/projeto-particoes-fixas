from models.processo import Processo
from services.sistema_memoria import SistemaMemoria

sistema = SistemaMemoria([100, 200, 300, 400])

print("===== SIMULAÇÃO DE PARTIÇÕES FIXAS =====\n")

# Preenchimento de todas as partições
p1 = Processo("P1", 80, 0)
p2 = Processo("P2", 150, 0)
p3 = Processo("P3", 270, 0)
p4 = Processo("P4", 380, 0)

sistema.alocar(p1)
sistema.alocar(p2)
sistema.alocar(p3)
sistema.alocar(p4)

# Tentar alocar com memória cheia (vai para a fila)
p5 = Processo("P5", 90, 0)
p6 = Processo("P6", 180, 0)
p7 = Processo("P7", 50, 0)

sistema.alocar(p5)
sistema.alocar(p6)
sistema.alocar(p7)

# Libera algumas partições (swapping acontece)
sistema.liberar("P1")  
sistema.liberar("P3")

# Mais alocações
p8 = Processo("P8", 290, 0)
p9 = Processo("P9", 60,  0)

sistema.alocar(p8)
sistema.alocar(p9)

sistema.liberar("P2")
sistema.liberar("P4")
sistema.liberar("P5")
sistema.liberar("P6")

sistema.relatorio()
