LIMITE_CONSUMO_ALTO = 200
SETORES_CRITICOS = {"habitacao", "comunicacao", "suporte_medico"}

sensores = [
    {"habitacao": "a", "carga": 10},
    {"comunicacao": "b", "carga": 15},
    {"suporte_medico": "c", "carga": 25}
]

def consumo_alto(registro):
    return registro["indicador"] == "energia" and registro["valor"] > LIMITE_CONSUMO_ALTO

def setor_critico(registro):
    return registro["setor"] in SETORES_CRITICOS

def gerar_alerta(registro):
    return consumo_alto(registro) and setor_critico(registro)

print("habitacao" in SETORES_CRITICOS)
print(LIMITE_CONSUMO_ALTO)

testes = [
    {"indicador": "energia", "valor": 150, "setor": "comunicacao"},
    {"indicador": "energia", "valor": 230, "setor": "habitacao"},
    {"indicador": "energia", "valor": 250, "setor": "laboratorio"},
    {"indicador": "energia", "valor": 90, "setor": "agricultura"}
]

if __name__ == "__main__":
    for teste in testes:
        print(
            f"Valor: {teste['valor']}, "
            f"setor: {teste['setor']}, "
            f"alerta: {gerar_alerta(teste)}"
        )
