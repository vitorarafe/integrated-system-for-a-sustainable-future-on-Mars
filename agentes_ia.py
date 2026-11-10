
from crud import listar_registros
from regras_logicas import filtrar_alertas
from estruturas import indexar_por_setor


historico = []

proibidas = ["desligar", "desativar", "ignorar alerta", "senha"]


def guardrail(pergunta):
    for p in proibidas:
        if p in pergunta.lower():
            return True
    return False


def triador(pergunta):
    texto = pergunta.lower()
    if "alerta" in texto:
        return "alertas"
    if "energia" in texto or "consumo" in texto:
        return "energia"
    if "setor" in texto:
        return "dados"
    return "nenhum"


def agente_energia(registros):
    total = 0
    quantidade = 0
    for r in registros:
        if r["indicador"].strip().lower() == "energia":
            total = total + r["valor"]
            quantidade = quantidade + 1
    if quantidade == 0:
        print("Agente de energia: nenhum registro de energia")
        return
    media = total / quantidade
    print("Agente de energia: total", total, "kWh | média", round(media, 1), "kWh")


def agente_alertas(registros):
    alertas = filtrar_alertas(registros)
    if len(alertas) == 0:
        print("Agente de alertas: nenhum alerta")
    for a in alertas:
        print("Agente de alertas: alerta em", a["setor"], "-", a["valor"], a["unidade"])


def agente_dados(pergunta, registros):
    indice = indexar_por_setor(registros)
    for setor in indice:
        if setor.replace("_", " ") in pergunta.lower() or setor in pergunta.lower():
            for r in indice[setor]:
                print("Agente de dados:", setor, "-", r["indicador"], r["valor"], r["unidade"])
            return
    print("Agente de dados: setor não encontrado")


def menu_agentes():
    print("\n=== Assistente com agentes (simulado) ===")
    print("Digite 'sair' para voltar ou 'historico' para ver as perguntas")
    while True:
        pergunta = input("\nPergunta: ").strip()
        if pergunta == "sair":
            break
        if pergunta == "historico":
            for h in historico:
                print("-", h)
            continue

        if guardrail(pergunta):
            print("Bloqueado pelo guardrail: ação insegura.")
            historico.append(pergunta + " (bloqueada)")
            continue

        registros = listar_registros()
        agente = triador(pergunta)
        historico.append(pergunta + " (" + agente + ")")

        if agente == "energia":
            agente_energia(registros)
            if len(filtrar_alertas(registros)) > 0:
                print("Handoff: energia -> alertas")
                agente_alertas(registros)
        elif agente == "alertas":
            agente_alertas(registros)
        elif agente == "dados":
            agente_dados(pergunta, registros)
        else:
            print("Não entendi. Pergunte sobre energia, alertas ou setor.")

        print("(Sugestão do sistema. A decisão final é humana.)")


if __name__ == "__main__":
    menu_agentes()