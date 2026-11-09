"""Operações CRUD para os indicadores sustentáveis da Aurora Siger."""

import math
import sqlite3

from database import conectar


def _validar_texto(campo: str, nome: str) -> str:
    texto = campo.strip()
    if not texto:
        raise ValueError(f"O campo '{nome}' não pode ficar vazio.")
    return texto


def _validar_valor(valor: str | float) -> float:
    try:
        numero = float(valor)
    except (TypeError, ValueError) as erro:
        raise ValueError("O valor deve ser um número.") from erro
    if not math.isfinite(numero) or numero < 0:
        raise ValueError("O valor deve ser finito e maior ou igual a zero.")
    return numero


def cadastrar_registro(
    indicador: str,
    valor: str | float,
    unidade: str,
    setor: str,
    observacoes: str = "",
) -> int:
    """Cadastra um indicador e retorna o ID gerado."""
    with conectar() as conexao:
        cursor = conexao.execute(
            """
            INSERT INTO registros_sustentabilidade
                (indicador, valor, unidade, setor, observacoes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                _validar_texto(indicador, "indicador"),
                _validar_valor(valor),
                _validar_texto(unidade, "unidade"),
                _validar_texto(setor, "setor"),
                observacoes.strip(),
            ),
        )
        return int(cursor.lastrowid)


def listar_registros() -> list[sqlite3.Row]:
    """Retorna todos os registros em ordem de cadastro."""
    with conectar() as conexao:
        return conexao.execute(
            """
            SELECT id, indicador, valor, unidade, setor, observacoes, criado_em
            FROM registros_sustentabilidade
            ORDER BY id
            """
        ).fetchall()


def atualizar_registro(
    registro_id: int,
    indicador: str,
    valor: str | float,
    unidade: str,
    setor: str,
    observacoes: str = "",
) -> bool:
    """Atualiza todos os campos do registro; retorna False se não existir."""
    with conectar() as conexao:
        cursor = conexao.execute(
            """
            UPDATE registros_sustentabilidade
            SET indicador = ?, valor = ?, unidade = ?, setor = ?, observacoes = ?
            WHERE id = ?
            """,
            (
                _validar_texto(indicador, "indicador"),
                _validar_valor(valor),
                _validar_texto(unidade, "unidade"),
                _validar_texto(setor, "setor"),
                observacoes.strip(),
                registro_id,
            ),
        )
        return cursor.rowcount > 0


def excluir_registro(registro_id: int) -> bool:
    """Exclui um registro pelo ID; retorna False se não existir."""
    with conectar() as conexao:
        cursor = conexao.execute(
            "DELETE FROM registros_sustentabilidade WHERE id = ?",
            (registro_id,),
        )
        return cursor.rowcount > 0
