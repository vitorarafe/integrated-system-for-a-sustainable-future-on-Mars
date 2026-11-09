"""Conexão e estrutura do banco de dados local do SIFSM."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


CAMINHO_BANCO = Path(__file__).with_name("sifsm.db")


@contextmanager
def conectar() -> Iterator[sqlite3.Connection]:
    """Abre uma conexão, confirma transações válidas e sempre a fecha."""
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    try:
        yield conexao
    except BaseException:
        conexao.rollback()
        raise
    else:
        conexao.commit()
    finally:
        conexao.close()


def inicializar_banco() -> None:
    """Cria a tabela de indicadores caso ela ainda não exista."""
    with conectar() as conexao:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS registros_sustentabilidade (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                indicador TEXT NOT NULL CHECK (length(trim(indicador)) > 0),
                valor REAL NOT NULL CHECK (valor >= 0),
                unidade TEXT NOT NULL CHECK (length(trim(unidade)) > 0),
                setor TEXT NOT NULL CHECK (length(trim(setor)) > 0),
                observacoes TEXT NOT NULL DEFAULT '',
                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
