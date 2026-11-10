import numpy as np
import matplotlib.pyplot as plt


def executar_modelo_linear():
    # --- Dados (simulados) ---
    tripulantes = np.array([2, 3, 4, 5, 6, 7, 8, 9, 10])
    consumo = np.array([95, 108, 112, 130, 135, 150, 160, 165, 182])

    # --- Achar a melhor reta ---
    # polyfit com grau 1 = reta. Devolve a (inclinação) e b (ponto inicial)
    a, b = np.polyfit(tripulantes, consumo, 1)
    previsto = a * tripulantes + b          # o que a reta "acha" para cada ponto

    print("\n--- MODELO LINEAR: CONSUMO x TRIPULANTES ---")
    print(f"Reta encontrada: consumo = {a:.2f} x tripulantes + {b:.2f}")

    # --- Análise exploratória: correlação ---
    correlacao = np.corrcoef(tripulantes, consumo)[0, 1]
    print(f"Correlação: {correlacao:.3f}")

    # --- Avaliação do modelo ---
    erro_medio = np.mean(np.abs(consumo - previsto))       # erro médio em kWh
    soma_erros = np.sum((consumo - previsto) ** 2)         # o que a reta errou
    soma_total = np.sum((consumo - consumo.mean()) ** 2)   # variação total dos dados
    r2 = 1 - soma_erros / soma_total
    print(f"Erro médio: {erro_medio:.2f} kWh")
    print(f"R²: {r2:.3f}")

    # --- Previsão para um valor novo ---
    novo = 12
    estimativa = a * novo + b
    print(f"Previsão para {novo} tripulantes: {estimativa:.1f} kWh")

    # --- Gráfico ---
    plt.figure()
    plt.scatter(tripulantes, consumo, label="Dados")
    plt.plot(tripulantes, previsto, color="red", label="Reta da regressão")
    plt.xlabel("Número de tripulantes")
    plt.ylabel("Consumo diário (kWh)")
    plt.title("Regressão linear: consumo x tripulantes")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    executar_modelo_linear()