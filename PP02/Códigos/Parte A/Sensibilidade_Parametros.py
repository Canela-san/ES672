import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import zero_Celsius
from Modelo_Turbina_ASE50 import *
from Dados_Iniciais import *


def main():
    variation = 0.1 # Variação de +- 40%
    n_points = 50
    indice = 0 # define o que será calculado: Potencia, Eficiencia termica ou Temperatua do gás de saída
    print(propriedades_fixas)
    
    plotar_gráfico(propriedades_fixas, params_ajuste, param_names_v, indice, legenda[indice], variation, n_points)

def plotar_gráfico(propriedades_fixas, params_ajuste, param_names_v, indice, legenda, variation, n_points):
    x_vals = 0
    # y_vals = [[0] * n_points]* len(params_ajuste.keys())
    y_vals = [[0 for _ in range(n_points)] for _ in range(len(params_ajuste.keys()))]
    temp = [np.array([])] * len(params_ajuste.keys())

    for j,param in enumerate(params_ajuste):
        x_vals = np.linspace(
            params_ajuste[param] * (1 - variation),
            params_ajuste[param] * (1 + variation),
            n_points
        )

        for i, val in enumerate(x_vals):
            p = params_ajuste.copy()
            p[param] = val
            y_vals[j][i] = Modelo_Turbina_ASE50(**propriedades_fixas, **p)

    x_percent = np.linspace((variation*(-100)), (variation*(100)), n_points)
    
    
    
    for j in range(len(params_ajuste.keys())):
        for i in range(n_points):
            temp[j] = np.append(temp[j], y_vals[j][i][indice])
        plt.plot(x_percent, temp[j], marker='o', markersize=3, label=param_names_v[j])
        # plt.plot(x_percent, temp1, marker='o', markersize=3, label='Sensor 1')    
    
    # plt.plot(x_percent, temp , marker='o')
    # plt.plot(x_percent, temp , marker='o')

    plt.legend()
    plt.xlabel(legenda[0])
    plt.ylabel(legenda[1])
    plt.title(legenda[2])
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()