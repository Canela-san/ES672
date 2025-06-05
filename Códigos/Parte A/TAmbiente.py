import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import zero_Celsius
from Modelo_Turbina_ASE50 import *
from Dados_Iniciais import *


def main():
    variation = 0.1 # Variação de +- 40%
    n_points = 50
    indice = 3 # define o que será calculado: Potencia, Eficiencia termica ou Temperatua do gás de saída
    propriedade = 'T_max'
    params_ajuste = {'perda_carga_ar_combustão': np.float64(1.4637794450670145), 'T_max': np.float64(1365.838519043944), 'eta_comp': np.float64(0.8446615021146631), 'eta_turb': np.float64(0.8887808893664478), 'rendimento_mecânico': np.float64(0.8666943779345587), 'perda_exaustao': np.float64(29.277409918315872)}
    propriedades = params_ajuste | propriedades_fixas
    x_vals = np.linspace(
            1045,
            1365.838519043944,
            n_points
        )
    y_vals = [0 for _ in range(n_points)]
    
    for i, val in enumerate (x_vals):
        propriedades[propriedade] = val
        y_vals[i] = Modelo_Turbina_ASE50(**propriedades)[indice]

    for i, val in enumerate(x_vals):
        x_vals[i] = x_vals[i] - zero_Celsius

    plt.plot(x_vals, y_vals, marker='o', markersize=3)
    plt.legend()
    plt.xlabel('Temperatura Máxima do Ciclo (C)')
    plt.ylabel('Fluxo de combustível (kg/s)')
    plt.title('Fluxo de combustível x Temperatura Máxima')
    plt.grid(True)
    plt.show()
    
    
main()