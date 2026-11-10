# SIFSM — Sistema Integrado de Futuro Sustentável em Marte

Protótipo em Python desenvolvido para a atividade integradora **"Futuro Sustentável em Marte"** (FIAP, 2026). O sistema organiza os registros da colônia **Aurora Siger**, aplica regras lógicas para detectar riscos, organiza alertas em estruturas de dados, simula a bateria da colônia, estima o consumo com regressão linear e oferece um assistente com agentes simulados.

> Nesta entrega, todos os dados são **simulados**. Não há sensores físicos nem serviços externos, e a IA é representada por agentes baseados em regras (sem modelo de linguagem).

## Entregas da atividade

| Requisito do enunciado | Implementação |
|---|---|
| Banco de dados e CRUD | `database.py` e `crud.py` (SQLite, tabela `registros_sustentabilidade`). |
| Tratamento de erros | `try/except/else/finally` em `codigo_fonte.py`, validações em `crud.py` e `rollback` em `database.py`. |
| Regra booleana | `regras_logicas.py` (alerta = consumo alto **E** setor crítico). |
| Circuito lógico | Simulação no Tinkercad com Arduino (`link_tinkercad.txt` e `circuito_logico.png`). |
| Estruturas de dados | `estruturas.py` (fila, heap de prioridade e tabela hash). |
| Simulação computacional e integração numérica | `simulacao_computacional.py` (bateria e regra do trapézio). |
| Modelo linear | `regressao_linear.py` (consumo por ciclo) e `modelo_linear.py` (consumo por tripulantes). |
| Integração de IA | `agentes_ia.py` (triador, especialistas, handoff, guardrails e histórico). |
| Arquitetura computacional e impacto socioambiental | Seções 9 e 10 do `relatorio_tecnico`. |
| Menu e integração | `codigo_fonte.py`. |

## Dependências

- Python 3.10 ou superior
- SQLite (já incluído no Python)
- NumPy
- Matplotlib

Crie o ambiente virtual com:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

Em seguida, instale as dependências:

```bash
pip install -r requirements.txt
```

## Como executar

Inicie o sistema com:

```bash
python codigo_fonte.py
```

Na primeira execução, o banco `sifsm.db` é criado automaticamente. Para ver o sistema funcionando, cadastre registros pela opção 1 ou use o banco que acompanha a entrega, já preenchido com os dados de exemplo de `dados_aurora_siger.csv`.

> Os gráficos (simulação e regressão) abrem em janelas do Matplotlib. Feche a janela do gráfico para o menu continuar.

## Menu do sistema

| Opção | Funcionalidade |
|---|---|
| 1 | Cadastrar registro |
| 2 | Listar registros |
| 3 | Alterar registro |
| 4 | Excluir registro |
| 5 | Analisar alertas (regra lógica, fila e heap) |
| 6 | Tabela verdade e circuito lógico |
| 7 | Simulação da bateria da colônia |
| 8 | Modelo linear: consumo por ciclo |
| 9 | Modelo linear: consumo por tripulantes |
| 10 | Assistente com agentes |
| 11 | Analisar sustentabilidade da colônia (fluxo completo) |
| 0 | Sair |

## Fluxo da análise de sustentabilidade (opção 11)

1. **Consulta de registros:** o sistema lê os registros do banco de dados.
2. **Regra lógica:** cada registro passa pela regra de alerta.
3. **Estruturas de dados:** os alertas entram em uma fila (ordem de chegada) e em um heap (ordem de urgência).
4. **Simulação:** a bateria é simulada em quatro cenários (normal, economia, tempestade de poeira e tempestade com economia).
5. **Modelo linear:** a análise exploratória e a avaliação do modelo estimam a tendência de consumo.
6. **Recomendação:** o sistema exibe uma recomendação técnica e as limitações. A decisão final é sempre humana.

## Regra lógica e circuito

A regra principal é: **emitir alerta quando o consumo de energia estiver alto E o setor for crítico.**

- `A`: consumo alto (registro de energia acima de 200 kWh).
- `B`: setor crítico (habitação, comunicação ou suporte médico).
- `S`: alerta, com `S = A · B`.

| A | B | S |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

No Tinkercad, a mesma lógica foi montada com um Arduino Uno: botões nos pinos 2 (A) e 3 (B), com `INPUT_PULLUP`, e um LED no pino 13 (S). O LED só acende quando A e B estão ativos.

## Estruturas de dados

| Estrutura | Onde é usada | Motivo da escolha |
|---|---|---|
| Fila (FIFO) | Atender os alertas por ordem de chegada. | Inserção e remoção em O(1). |
| Heap de prioridade | Atender primeiro o alerta de maior consumo. | Extração do mais urgente em O(log n). |
| Tabela hash (dicionário) | Buscar registros por setor (usada pelo agente de dados). | Busca por chave em tempo médio O(1). |

## Simulação computacional

A simulação representa um dia marciano (24,65 h) com passo de 3 minutos. A energia consumida é calculada pela **regra do trapézio** (integração numérica) e o estado de carga da bateria (400 kWh de capacidade) é atualizado a cada passo. Quatro cenários são comparados: normal, economia de 20%, tempestade de poeira e tempestade com economia. O gráfico mostra o estado de carga e o limite mínimo seguro de 20%.

## Modelagem linear

| Modelo | Arquivo | Resultado |
|---|---|---|
| Consumo por ciclo (15 ciclos, treino com 12 e teste com 3) | `regressao_linear.py` | Consumo = 112,70 + 7,29 x Ciclo. MAE 1,22, RMSE 1,36 e R² 0,9616 no teste. |
| Consumo por tripulantes (2 a 10) | `modelo_linear.py` | Consumo = 10,58 x tripulantes + 73,94. Erro médio 2,45 kWh e R² 0,990. |

Os dados são simulados e regulares, por isso os R² são altos. O segundo modelo foi avaliado nos mesmos dados do ajuste, e as previsões servem como apoio, não como decisão automática.

## Agentes de IA (simulados)

| Componente | Função |
|---|---|
| Guardrail | Bloqueia pedidos inseguros (desligar, desativar, ignorar alerta, senha). |
| Agente triador | Encaminha a pergunta ao especialista correto. |
| Agente de energia | Soma e calcula a média dos registros de energia. |
| Agente de alertas | Lista os alertas pela regra booleana. |
| Agente de dados | Busca registros por setor usando a tabela hash. |
| Handoff | O agente de energia encaminha ao agente de alertas quando há alertas. |
| Histórico | Guarda as perguntas da sessão (comando `historico`). |

Exemplos de perguntas: "qual o consumo de energia?", "tem algum alerta?", "dados do setor habitação".

## Como testar módulos separadamente

```bash
python regras_logicas.py
python simulacao_computacional.py
python regressao_linear.py
python modelo_linear.py
python agentes_ia.py
```

## Estrutura do projeto

```text
codigo_fonte.py              Programa principal (menu)
database.py                  Conexão e criação do banco
crud.py                      Operações CRUD com validação
regras_logicas.py            Regra booleana e tabela verdade
estruturas.py                Fila, heap e tabela hash
simulacao_computacional.py   Simulação da bateria
regressao_linear.py          Regressão linear (consumo por ciclo)
modelo_linear.py             Regressão linear (consumo por tripulantes)
agentes_ia.py                Agentes, guardrails e histórico
script_banco.sql             Criação da tabela
dados_aurora_siger.csv       Dados simulados de exemplo
circuito_logico.png          Imagem do circuito
link_tinkercad.txt           Link da simulação no Tinkercad
relatorio_tecnico.pdf        Relatório técnico
link_video.txt               Link do vídeo (YouTube, não listado)
graficos_ou_imagens/         Prints e gráficos de execução
requirements.txt             Dependências
```

## Limitações

- Dados simulados e em pequena quantidade; limites como 200 kWh são ilustrativos.
- Modelos lineares com uma variável e poucos pontos.
- Simulação com potências em degraus e sem perdas da bateria.
- Agentes baseados em palavras-chave, com histórico apenas em memória.
- A decisão final sobre qualquer alerta ou recomendação é humana.

## Vídeo de apresentação

O link do vídeo (YouTube, não listado) está no arquivo `link_video.txt`.

---
## Autor

```bash
Integrantes
Nome: ANA CAROLINA FREIRE MAFRA – rm573650
Nome: Daniel Guimarães Barreto – rm573425
Nome: Paulo Henrique da Silva Gola – rm572992
Nome: Vinicius Daniel de Borba – rm572091
Nome: Vitor de Araujo Ferreira – rm572838
```

---

Projeto desenvolvido para fins acadêmicos na atividade integradora "Futuro Sustentável em Marte", FIAP, 2026.
