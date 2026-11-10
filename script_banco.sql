CREATE TABLE IF NOT EXISTS registros_sustentabilidade (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    indicador TEXT NOT NULL CHECK (length(trim(indicador)) > 0),
    valor REAL NOT NULL CHECK (valor >= 0),
    unidade TEXT NOT NULL CHECK (length(trim(unidade)) > 0),
    setor TEXT NOT NULL CHECK (length(trim(setor)) > 0),
    observacoes TEXT NOT NULL DEFAULT '',
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);