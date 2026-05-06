# 🧠 Simulador de Partições Fixas de Memória

Simulador de gerenciamento de memória com **partições fixas**, fila de espera e swapping.  
Desenvolvido em Python puro como trabalho da disciplina de Sistemas Operacionais.

---

## 📋 Descrição

O sistema simula a alocação de processos em partições fixas de tamanhos diferentes (100, 200, 300 e 400 unidades). Quando todas as partições estão ocupadas, os processos entram em uma **fila de espera** e são alocados automaticamente via **swapping** quando uma partição é liberada.

### Funcionalidades
- Alocação por **First-Fit** (primeira partição livre com tamanho suficiente)
- **Fila de espera** quando nenhuma partição atende o processo
- **Swapping automático** ao liberar uma partição
- **Relatório de métricas** ao final da simulação

---

## 🗂️ Estrutura do Projeto

```
projeto-particoes-fixas/
├── src/
│   ├── models/
│   │   ├── processo.py       # Classe Processo
│   │   └── particao.py       # Classe Partição
│   ├── services/
│   │   └── sistema_memoria.py  # Lógica principal do simulador
│   └── main.py               # Simulação e ponto de entrada
└── README.md
```

---

## ✅ Pré-requisitos

- Python 3.6 ou superior

Verifique sua versão com:
```bash
python3 --version
```

---

## 🚀 Como Rodar

### 1. Clone o repositório

```bash
git clone https://github.com/neyadrian/projeto-particoes-fixas.git
```

### 2. Entre na pasta do projeto

```bash
cd projeto-particoes-fixas
```

### 3. Acesse a pasta src

```bash
cd src
```

### 4. Execute a simulação

```bash
python main.py
```

> **Nota:** dependendo do sistema, use `python3` no lugar de `python`

---

## 📊 Saída Esperada

```
===== SIMULAÇÃO DE PARTIÇÕES FIXAS =====

[Ciclo 1] Processo P1 (80u) -> Partição 0 (100u)
[Ciclo 2] Processo P2 (150u) -> Partição 1 (200u)
[Ciclo 3] Processo P3 (270u) -> Partição 2 (300u)
[Ciclo 4] Processo P4 (380u) -> Partição 3 (400u)
[Ciclo 5] Processo P5 (90u) -> FILA DE ESPERA
[Ciclo 6] Processo P6 (180u) -> FILA DE ESPERA
[Ciclo 7] Processo P7 (50u) -> FILA DE ESPERA
[Ciclo 8] Processo P1 liberou Partição 0
[Ciclo 8] Processo P5 saiu da fila -> Partição 0
...

========== RELATÓRIO FINAL ==========
Processos que entraram na fila: 3
Tempo médio de espera: 3.00 ciclos
Utilização média das partições: 85.00%
Fragmentação interna total: 3.00%
=====================================
```

---

## 📐 Métricas Geradas

| Métrica | Descrição |
|---|---|
| Processos na fila | Total de processos que não foram alocados imediatamente |
| Tempo médio de espera | Média de ciclos que os processos aguardaram na fila |
| Utilização média | Percentual médio de uso das partições ocupadas |
| Fragmentação interna | Memória desperdiçada dentro das partições ocupadas |

---

## 🔬 Conceitos Implementados

### Partições Fixas
Divisão da memória em regiões de tamanho imutável. Cada partição só pode conter um processo por vez.

### First-Fit
O processo é alocado na **primeira** partição livre que seja grande o suficiente para ele.

### Swapping
Ao liberar uma partição, o sistema verifica automaticamente a fila de espera e aloca o primeiro processo que caiba.

### Fragmentação Interna
Ocorre quando o processo é menor que a partição. O espaço excedente fica inutilizado.

---

## 👨‍💻 Autor

Desenvolvido por **Neyadrian** — Sistemas Operacionais
