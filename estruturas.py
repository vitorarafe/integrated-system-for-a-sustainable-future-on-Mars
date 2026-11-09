"""Estruturas de dados do SIFSM"""

from collections import deque
import heapq

class FilaAlertas:
    """Fila (FIFO): Ordem de chegada."""
    def __init__(self):
        self._itens = deque()

    def enfileirar(self, alerta):
        self._itens.append(alerta)

    def desenfileirar(self):
        return self._itens.popleft() if self._itens else None

    def vazia(self):
        return len(self._itens) == 0

    def __len__(self):
        return len(self._itens)

class HeapPrioridade:
    """Heap: o alerta mais urgente sai primeiro."""
    def __init__(self):
        self._heap = []
        self._contador = 0   # desempata prioridades iguais (ordem de chegada)

    def inserir(self, alerta, prioridade):
        # heapq é min-heap, então usamos -prioridade para o maior sair primeiro
        heapq.heappush(self._heap, (-prioridade, self._contador, alerta))
        self._contador += 1

    def extrair_maior(self):
        return heapq.heappop(self._heap)[2] if self._heap else None

    def __len__(self):
        return len(self._heap)

def indexar_por_setor(registros):
    """Tabela hash (dict): busca instantânea dos registros de um setor."""
    indice = {}
    for registro in registros:
        indice.setdefault(registro["setor"], []).append(registro)
    return indice