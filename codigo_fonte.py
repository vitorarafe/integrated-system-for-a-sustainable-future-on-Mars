"""Interface de linha de comando do Sistema Integrado de Futuro Sustentável em Marte."""

import sqlite3
import agentes_ia
import modelo_linear
import regressao_linear
import simulacao_computacional
from regras_logicas import filtrar_alertas, tabela_verdade
from estruturas import FilaAlertas, HeapPrioridade

from crud import (
    atualizar_registro,
    cadastrar_registro,
    excluir_registro,
    listar_registros,
)
from database import inicializar_banco


def exibir_registros() -> None:
    registros = listar_registros()
    if not registros:
        print("Nenhum registro cadastrado.")
        return

    print("\nID | Indicador | Valor | Unidade | Setor | Observações | Criado em")
    print("-" * 100)
    for registro in registros:
        print(
            f"{registro['id']} | {registro['indicador']} | "
            f"{registro['valor']:g} | {registro['unidade']} | "
            f"{registro['setor']} | {registro['observacoes']} | "
            f"{registro['criado_em']}"
        )


def cadastrar() -> None:
    indicador = input("Indicador (ex.: água, energia ou produção): ").strip()
    valor = input("Valor medido: ").strip()
    unidade = input("Unidade de medida (ex.: L, kWh, kg): ").strip()
    setor = input("Setor da colônia: ").strip()
    observacoes = input("Observações (opcional): ").strip()

    registro_id = cadastrar_registro(
        indicador, valor, unidade, setor, observacoes
    )
    print(f"Registro {registro_id} cadastrado.")


def atualizar() -> None:
    registro_id = int(input("ID do registro a alterar: ").strip())
    indicador = input("Novo indicador: ").strip()
    valor = input("Novo valor: ").strip()
    unidade = input("Nova unidade: ").strip()
    setor = input("Novo setor: ").strip()
    observacoes = input("Novas observações (opcional): ").strip()

    if atualizar_registro(
        registro_id, indicador, valor, unidade, setor, observacoes
    ):
        print("Registro alterado.")
    else:
        print("Registro não encontrado.")


def excluir() -> None:
    registro_id = int(input("ID do registro a excluir: ").strip())
    if excluir_registro(registro_id):
        print("Registro excluído.")
    else:
        print("Registro não encontrado.")

def analisar_alertas() -> None:
    registros = listar_registros()
    alertas = filtrar_alertas(registros)
    if not alertas:
        print("Nenhum alerta: nenhum setor crítico com consumo alto.")
        return

    fila = FilaAlertas()
    heap = HeapPrioridade()
    for alerta in alertas:
        fila.enfileirar(alerta)
        heap.inserir(alerta, alerta["valor"])

    print(f"\n{len(alertas)} alerta(s) detectado(s).")
    print("\nOrdem de chegada (fila):")
    while not fila.vazia():
        a = fila.desenfileirar()
        print(f" - {a['setor']}: {a['valor']:g} {a['unidade']}")

    print("\nOrdem de urgência (heap):")
    while len(heap) > 0:
        a = heap.extrair_maior()
        print(f" - {a['setor']}: {a['valor']:g} {a['unidade']}")

def explicar_circuito() -> None:
    print("\n=== Circuito lógico (Arduino / Tinkercad) ===")
    print("Entradas: botão A (pino 2) = consumo alto | botão B (pino 3) = setor crítico")
    print("Saída: LED (pino 13) = alerta")
    print("Regra: S = A E B (o LED só acende se A e B estiverem ativos)")
    print("Link do circuito: [colar o link do Tinkercad]")
    tabela_verdade()


def analisar_sustentabilidade() -> None:
    print("\n=== ANÁLISE DE SUSTENTABILIDADE DA COLÔNIA ===")

    print("\n[1/4] Registros, regra lógica e estruturas de dados")
    exibir_registros()
    analisar_alertas()

    print("\n[2/4] Simulação da bateria (feche o gráfico para continuar)")
    simulacao_computacional.executar_simulacao()

    print("\n[3/4] Previsão de consumo (regressão linear)")
    regressao_linear.analise_exploratoria()
    regressao_linear.avaliar_modelo()

    print("\n[4/4] Conclusão")
    alertas = filtrar_alertas(listar_registros())
    if alertas:
        print(f"Recomendação: {len(alertas)} registro(s) crítico(s) acima do limite. "
              "Priorizar o de maior consumo e avaliar economia de energia.")
    else:
        print("Recomendação: manter o monitoramento; nenhum setor crítico acima do limite.")
    print("Limitações: dados simulados, modelos lineares simples, agentes por regras.")
    print("A decisão final deve ser validada por um responsável humano.")

def executar() -> None:
    try:
        inicializar_banco()
    except sqlite3.Error as erro:
        print(f"Não foi possível inicializar o banco de dados: {erro}")
        return

    while True:
        print(
            "\n=== SIFSM | Dados sustentáveis da Aurora Siger ===\n"
            "1. Cadastrar registro\n"
            "2. Listar registros\n"
            "3. Alterar registro\n"
            "4. Excluir registro\n"
            "5. Analisar alertas (regra lógica)\n"
            "6. Tabela verdade e circuito lógico\n"
            "7. Simulação da bateria\n"
            "8. Modelo linear: consumo por ciclo\n"
            "9. Modelo linear: consumo por tripulantes\n"
            "10. Assistente com agentes\n"
            "11. Analisar sustentabilidade da colônia\n"
            "0. Sair"
        )
        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                cadastrar()
            elif opcao == "2":
                exibir_registros()
            elif opcao == "3":
                atualizar()
            elif opcao == "4":
                excluir()
            elif opcao == "5":
                analisar_alertas()
            elif opcao == "6":
                explicar_circuito()
            elif opcao == "7":
                simulacao_computacional.executar_simulacao()
            elif opcao == "8":
                regressao_linear.menu()
            elif opcao == "9":
                modelo_linear.executar_modelo_linear()
            elif opcao == "10":
                agentes_ia.menu_agentes()
            elif opcao == "11":
                analisar_sustentabilidade()
            elif opcao == "0":
                print("Encerrando o SIFSM.")
                break
            else:
                raise ValueError("Opção inválida. Escolha um número do menu.")
        except (ValueError, sqlite3.Error) as erro:
            print(f"Erro: {erro}")
        else:
            print("Operação concluída.")
        finally:
            print()

if __name__ == "__main__":
    executar()
