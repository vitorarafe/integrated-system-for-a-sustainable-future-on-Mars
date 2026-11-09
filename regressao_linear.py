
import math

# Dados simulados de consumo energetico da colonia
# Cada registro representa um ciclo de operacao
ciclos = list(range(1, 16))

consumo = [
    120, 128, 135, 141, 150,
    155, 164, 170, 179, 185,
    193, 201, 207, 216, 224
]


# Calcula a media de uma lista
def calcular_media(valores):
    return sum(valores) / len(valores)


# Calcula a correlacao entre duas variaveis
def calcular_correlacao(x, y):
    media_x = calcular_media(x)
    media_y = calcular_media(y)

    numerador = sum(
        (x[i] - media_x) * (y[i] - media_y)
        for i in range(len(x))
    )

    denominador = math.sqrt(
        sum((v - media_x) ** 2 for v in x) *
        sum((v - media_y) ** 2 for v in y)
    )

    if denominador == 0:
        return 0

    return numerador / denominador


# Ajusta a regressao linear pelo metodo dos minimos quadrados
def treinar_modelo(x, y):
    media_x = calcular_media(x)
    media_y = calcular_media(y)

    numerador = sum(
        (x[i] - media_x) * (y[i] - media_y)
        for i in range(len(x))
    )

    denominador = sum(
        (valor - media_x) ** 2 for valor in x
    )

    if denominador == 0:
        raise ValueError("Nao e possivel ajustar o modelo.")

    b1 = numerador / denominador
    b0 = media_y - b1 * media_x

    return b0, b1


# Faz uma previsao
def prever_consumo(ciclo, b0, b1):
    return b0 + b1 * ciclo


# Avalia o modelo com dados de test
def avaliar_modelo():
    x_treino = ciclos[:12]
    y_treino = consumo[:12]

    x_teste = ciclos[12:]
    y_teste = consumo[12:]

    b0, b1 = treinar_modelo(x_treino, y_treino)

    previsoes = [
        prever_consumo(x, b0, b1)
        for x in x_teste
    ]

    erros = [
        real - previsto
        for real, previsto in zip(y_teste, previsoes)
    ]

    mae = sum(abs(e) for e in erros) / len(erros)
    mse = sum(e ** 2 for e in erros) / len(erros)
    rmse = math.sqrt(mse)

    media_real = calcular_media(y_teste)

    soma_total = sum(
        (valor - media_real) ** 2 for valor in y_teste
    )

    soma_erros = sum(e ** 2 for e in erros)

    r2 = 1 - soma_erros / soma_total if soma_total else 0

    print("\n===== AVALIACAO DO MODELO =====")
    print(f"MAE: {mae:.2f}")
    print(f"MSE: {mse:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2: {r2:.4f}")

    print("\nConsumo real x previsto:")

    for real, previsto in zip(y_teste, previsoes):
        print(f"Real: {real:.2f} | Previsto: {previsto:.2f}")

    return b0, b1


# Analise exploratoria
def analise_exploratoria():
    print("\n===== ANALISE EXPLORATORIA =====")

    print(f"Total de registros: {len(consumo)}")
    print(f"Consumo medio: {calcular_media(consumo):.2f} kWh")
    print(f"Menor consumo: {min(consumo)} kWh")
    print(f"Maior consumo: {max(consumo)} kWh")

    correlacao = calcular_correlacao(ciclos, consumo)

    print(f"Correlacao entre ciclo e consumo: {correlacao:.4f}")

    if correlacao > 0:
        print("O consumo apresenta tendencia de crescimento.")
    else:
        print("O consumo apresenta tendencia de queda.")


# Menu
def menu():
    b0, b1 = treinar_modelo(ciclos[:12], consumo[:12])

    while True:
        print("\n================================")
        print(" AURORA SIGER - SIFSM")
        print(" MODULO DE REGRESSAO LINEAR")
        print("================================")
        print("1 - Analise exploratoria")
        print("2 - Visualizar equacao linear")
        print("3 - Avaliar modelo")
        print("4 - Prever consumo futuro")
        print("0 - Sair")

        opcao = input("\nEscolha uma opcao: ")

        if opcao == "1":
            analise_exploratoria()

        elif opcao == "2":
            print("\n===== EQUACAO DO MODELO =====")
            print(f"Consumo = {b0:.2f} + ({b1:.2f} x Ciclo)")
            print(f"Coeficiente angular: {b1:.2f}")
            print("O coeficiente indica a variacao estimada")
            print("do consumo a cada novo ciclo.")

        elif opcao == "3":
            avaliar_modelo()

        elif opcao == "4":
            try:
                ciclo = int(input("Digite o ciclo futuro: "))

                if ciclo <= 0:
                    print("O ciclo deve ser maior que zero.")
                    continue

                previsao = prever_consumo(ciclo, b0, b1)

                print(f"\nConsumo estimado: {previsao:.2f} kWh")

                if previsao > 200:
                    print("ALERTA: consumo elevado!")
                    print("Recomendacao: avaliar economia de energia.")
                else:
                    print("Consumo dentro do limite ilustrativo.")

            except ValueError:
                print("Digite um numero inteiro valido.")

        elif opcao == "0":
            print("Encerrando o modulo Dandan.")
            break

        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    menu()