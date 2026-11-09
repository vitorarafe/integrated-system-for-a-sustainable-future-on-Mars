"""  Regras booleanas do SIFSM (Aurora Siger)  """

import unicodedata

#consts 
LIMITE_CONSUMO_ALTO = 200
SETORES_CRITICOS = {"habitacao", "comunicacao", "suporte_medico"}

def _normalizar(texto):
    """Retira acento, espaços nas pontas e maiúsculas."""
    sem_acento = unicodedata.normalize("NFD", str(texto))
    sem_acento = "".join(c for c in sem_acento if unicodedata.category(c) != "Mn")
    return sem_acento.strip().lower().replace(" ", "_")

sensores = [
    {"habitacao": "a", "carga": 10},
    {"comunicacao": "b", "carga": 15},
    {"suporte_medico": "c", "carga": 25}
]
# ---------- Entradas da regra (A e B da tabela verdade) ----------
def consumo_alto(registro):
    return _normalizar(registro["indicador"]) == "energia" and registro["valor"] > LIMITE_CONSUMO_ALTO

def setor_critico(registro):
    return _normalizar(registro["setor"]) in SETORES_CRITICOS

# ---------- Regra principal: S = A E B ----------
def gerar_alerta(registro):
    return consumo_alto(registro) and setor_critico(registro)

def filtrar_alertas(registros):
    """Percorre os registros e devolve só os que geram alerta."""
    alertas = []
    for registro in registros:
        if gerar_alerta(registro):
            alertas.append(registro)
    return alertas

def tabela_verdade():
    """Imprime a tabela verdade da regra (para o relatório e o vídeo)."""
    print("A (consumo alto) | B (setor critico) | S (alerta)")
    for a in (False, True):
        for b in (False, True):
            print(f"        {int(a)}        |         {int(b)}         |     {int(a and b)}")
            
if __name__ == "__main__":

    testes = [
    {"indicador": "energia", "valor": 150, "setor": "comunicacao"},
    {"indicador": "energia", "valor": 230, "setor": "habitacao"},
    {"indicador": "energia", "valor": 250, "setor": "laboratorio"},
    {"indicador": "energia", "valor": 90, "setor": "agricultura"}
]

    for t in testes:
        print(f"Valor: {t['valor']}, setor: {t['setor']}, alerta: {gerar_alerta(t)}")
    print("\nSó os alertas:", filtrar_alertas(testes))
    print()
    tabela_verdade()