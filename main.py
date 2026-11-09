"""Interface de linha de comando do Sistema Integrado de Futuro Sustentável em Marte."""

import sqlite3

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
