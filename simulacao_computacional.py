import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PARÂMETROS DO MODELO
# ============================================================
DURACAO_SOL_H = 24.65     # duração de um dia marciano (horas)
PASSO_H = 0.05            # passo de tempo (horas) = 3 minutos
CAPACIDADE_KWH = 400.0    # quanto a bateria guarda quando está 100% cheia
SOC_INICIAL = 80.0        # carga da bateria no início do sol (%)

# Cada cenário tem: (fator da geração, fator do consumo)
CENARIOS = {
    "Normal": (1.0, 1.0),
    "Economia (-20%)": (1.0, 0.8),
    "Tempestade de poeira": (0.3, 1.0),
    "Tempestade + economia": (0.3, 0.8),
}


# ============================================================
# CONSUMO E GERAÇÃO (potência em kW, por faixa de horário)
# ============================================================
def consumo_em(hora):
    """Recebe uma hora e devolve quantos kW a colônia consome."""
    if 6 <= hora < 10:        # manhã: laboratório e estufa
        return 28.0
    elif 18 <= hora < 22:     # noite: habitação e aquecimento
        return 32.0
    else:                     # resto do dia: só o consumo base
        return 18.0


def geracao_em(hora):
    """Recebe uma hora e devolve quantos kW os painéis solares geram."""
    if 6 <= hora < 18:        # horas de sol
        return 45.0
    else:                     # noite
        return 0.0


# ============================================================
# BATERIA (estado de carga, SoC)
# ============================================================
def simular_soc(t, p_ger, p_cons):
    """Simula a bateria passo a passo. Devolve o SoC (%) e o desperdício (kWh)."""
    soc = np.zeros(len(t))      # lista de zeros, uma posição por instante
    soc[0] = SOC_INICIAL        # primeiro valor: carga inicial
    desperdicio = 0.0           # energia gerada que não coube na bateria

    for i in range(len(t) - 1):
        saldo = p_ger[i] - p_cons[i]                      # kW: sobra (+) ou falta (-)
        energia = saldo * PASSO_H                         # kWh neste passo
        novo = soc[i] + energia / CAPACIDADE_KWH * 100    # novo SoC em %

        if novo > 100:                                    # bateria não passa de 100%
            desperdicio += (novo - 100) / 100 * CAPACIDADE_KWH
            novo = 100
        if novo < 0:                                      # nem fica abaixo de 0%
            novo = 0

        soc[i + 1] = novo                                 # guarda para o próximo passo

    return soc, desperdicio


# ============================================================
# FUNÇÃO PRINCIPAL (é esta que o menu vai chamar)
# ============================================================
def executar_simulacao():
    # Vetor de tempo: 0, 0.05, 0.10, ... até 24.65
    t = np.arange(0, DURACAO_SOL_H + PASSO_H, PASSO_H)

    # Potência de consumo e de geração em cada instante
    p_cons = np.array([consumo_em(h) for h in t])
    p_ger = np.array([geracao_em(h) for h in t])

    # Integral (regra do trapézio): energia = área sob a curva de potência
    energia_total = np.sum((p_cons[:-1] + p_cons[1:]) / 2 * np.diff(t))
    consumo_medio = energia_total / (t[-1] - t[0])

    print("\n--- SIMULAÇÃO DA BATERIA DA COLÔNIA ---")
    print(f"Energia consumida no sol: {energia_total:.1f} kWh")
    print(f"Consumo médio: {consumo_medio:.2f} kW")

    # Simula e compara os cenários
    plt.figure()
    for nome, (fator_ger, fator_cons) in CENARIOS.items():
        soc, desp = simular_soc(t, p_ger * fator_ger, p_cons * fator_cons)
        horas_baixo = np.sum(soc < 20) * PASSO_H
        print(f"{nome}: SoC final {soc[-1]:.1f}% | "
              f"mínimo {soc.min():.1f}% | "
              f"{horas_baixo:.1f} h abaixo de 20% | "
              f"desperdício {desp:.1f} kWh")
        plt.plot(t, soc, label=nome)

    # Gráfico comparando os cenários
    plt.axhline(20, color="red", linestyle="--", label="Mínimo seguro (20%)")
    plt.xlabel("Tempo (h)")
    plt.ylabel("Estado de carga (%)")
    plt.title("Bateria da colônia: comparação de cenários")
    plt.ylim(0, 105)
    plt.legend()
    plt.grid(True)
    plt.show()


# Só roda sozinho se você executar ESTE arquivo diretamente.
# Quando outro arquivo importa, não roda nada automaticamente.
if __name__ == "__main__":
    executar_simulacao()