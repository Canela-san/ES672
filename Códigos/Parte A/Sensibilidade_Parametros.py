import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import zero_Celsius
from Modelo_Turbina_ASE50 import *

def main():
    Fabricante= [3644,29.56,559]
    
    #propriedades fixas:
    propriedades_fixas = {
    'Patm': 101325,
    'fluxo_compressor': 14.16,
    'relação_pressões_compressão': 10.7,
    'PCI_do_gás_natural': 50.01 * 1000000,
    'T_ambiente': 15
    }
    
    params_ajuste = {
        'perda_carga_ar_combustão': 1.5,
        'T_max': 1078 + zero_Celsius,
        'eta_comp': 0.828,
        'eta_turb': 0.857,
        'rendimento_mecânico': 0.975,
        'perda_exaustao': 30
    }

    # Nome amigável para os eixos
    param_names = {
        'perda_carga_ar_combustao': 'Perda carga ar combustão',
        'T_max': 'Temperatura Máxima',
        'eta_comp': 'Eficiência Isentrópica Compressor',
        'eta_turb': 'Eficiência Isentrópica Expansão',
        'rendimento_mecânico': 'Rendimento Eletromecânico',
        'perda_exaustao': 'Perda de carga na exaustão'
    }
    param_names_v = list(param_names.values())

    # Variação de ±10%
    variation = 0.4
    n_points = 50
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
            y_vals[j][i] = pp02A(**propriedades_fixas, **p)

    x_percent = np.linspace((variation*(-100)), (variation*(100)), n_points)
    
    for j in range(len(params_ajuste.keys())):
        for i in range(n_points):
            temp[j] = np.append(temp[j], y_vals[j][i][0])
        plt.plot(x_percent, temp[j], marker='o', markersize=3, label=param_names_v[j])
        # plt.plot(x_percent, temp1, marker='o', markersize=3, label='Sensor 1')    
    
    # plt.plot(x_percent, temp , marker='o')
    # plt.plot(x_percent, temp , marker='o')

    legenda = {
        'Potência': ['Variação Percentual (%)','Potência Líquida (kW)','Potencia Líquida x Variação de Parâmetros'],
        'Eficiência': ['Variação Percentual (%)','Eficiência Térmica','Eficiência Térmica x Variação de Parâmetros'],
        'Temperatura': ['Variação Percentual (%)','Temperatura do Gás de Exaustão (C)','Temperatura do Gás de Exaustão x Variação de Parâmetros']
        
    }

    label = 'Potência'
    plt.legend()
    plt.xlabel(legenda[label][0])
    plt.ylabel(legenda[label][1])
    plt.title(legenda[label][2])
    plt.grid(True)
    plt.show()


    # # resposta = pp02A(**propriedades_fixas, **params_ajuste)


    # # printSI(Fabricante,resposta)
 
 
 
 
 
 
    # n_points = 10
    # y_vals = [0] * n_points
    # x_vals = np.linspace(
    #     0,
    #     40,
    #     n_points
    # )

    # for i, val in enumerate(x_vals):
    #     p = propriedades_fixas.copy()
    #     p['T_ambiente'] = val
    #     y_vals[i] = pp02A(**p, **params_ajuste)

    # y_vals = [list(linha) for linha in zip(*y_vals)]
    # plt.plot(x_vals, y_vals[2], marker='o')
    # plt.xlabel('Temperatura Ambiente (ºC)')
    # plt.ylabel('Temperatura dos Gases')
    # plt.title('Temperatura dos Gases x Temperatura')
    # plt.grid(True)
    # plt.show()


def printSI(Fabricante, resposta):
    Diferença = [100*(resposta[0]-Fabricante[0])/Fabricante[0],100*(resposta[1]-Fabricante[1])/Fabricante[1],100*(resposta[2]-Fabricante[2])/Fabricante[2]]

    # print(f"Potência Líquida {Potência_Líquida}")
    # print(f"Eficiência (%): {eficiência_Termica*100}")
    # print(f"Tgases (C): {t4-273.15}")
    # print()

    print(f"Fabricante: {Fabricante}")
    print(f"Simulação: {resposta}")
    print(f"Diferença: {Diferença}")

main()
