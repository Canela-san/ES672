import CoolProp.CoolProp as CP
import numpy as np
import matplotlib.pyplot as plt

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
        'T_max': 1078 + 273.15,
        'eta_comp': 0.828,
        'eta_turb': 0.857,
        'rendimento': 0.975,
        'perda_exaustao': 30
    }

    # Nome amigável para os eixos
    param_names = {
        'perda_carga_ar_combustao': 'Perda carga ar combustão',
        'T_max': 'Temperatura Máxima',
        'eta_comp': 'Eficiência Isentrópica Compressor',
        'eta_turb': 'Eficiência Isentrópica Expansão',
        'rendimento': 'Rendimento Eletromecânico',
        'perda_exaustao': 'Perda de carga na exaustão'
    }

    # Variação de ±10%
    variation = 0.1
    n_points = 10
    x_vals = 0
    y_vals = [[0] * n_points]* len(params_ajuste.keys())
    temp = [np.array([])] * 6

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
    
    for j in range(0,6):
        for i in range(0,n_points):
            temp[j] = np.append(temp[j], y_vals[j][i][0])
        plt.plot(x_percent, temp[j], marker='o')    
    
    # plt.plot(x_percent, temp , marker='o')
    # plt.plot(x_percent, temp , marker='o')


    plt.xlabel('perda_carga_ar_combustão (%)')
    plt.ylabel('Potência Elétrica Líquida')
    plt.title('Potencia x perda_carga_ar_combustão')
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


def pp02A(
        Patm,
        fluxo_compressor,
        relação_pressões_compressão,
        perda_carga_ar_combustão,
        PCI_do_gás_natural,
        T_max,
        perda_exaustao,
        eta_comp,
        eta_turb,
        rendimento,
        T_ambiente
        ):

    t1 = T_ambiente + 273.15
    p1 = Patm

    # compressor

    pressão_compressor = p1 * relação_pressões_compressão
    h1 = CP.PropsSI('H', 'T', t1, 'P', p1, 'Air')
    s1 = CP.PropsSI('S', 'T', t1, 'P', p1, 'Air')

    s2 = s1
    p2 = p1 * relação_pressões_compressão
    h2s = CP.PropsSI('H', 'S', s2, 'P', p2, 'Air')
    h2 = ((h2s - h1) / eta_comp) + h1
    t2 = CP.PropsSI('T', 'P', p2, 'H', h2, 'Air')
    potencia_compressor = fluxo_compressor * (h2 - h1)

    #camara de combustão

    p3 = (1-(perda_carga_ar_combustão/100))*pressão_compressor
    h3 = CP.PropsSI('H', 'P', p3, 'T', T_max, 'Air')
    Fluxo_massico_combustão=(fluxo_compressor*(h3-h2))/(PCI_do_gás_natural-(h3-h2))
    s3 = CP.PropsSI('S', 'P', p3, 'H', h3, 'Air')

    p4 = p1 + (perda_exaustao * 100)
    h4s = CP.PropsSI('H', 'S', s3, 'P', p4, 'Air')
    h4 = h3-(eta_turb*(h3-h4s))
    t4 = CP.PropsSI('T', 'H', h4, 'P', p4, 'Air')
    potencia_expansor = (fluxo_compressor+Fluxo_massico_combustão)*(h3-h4)

    #Conclusão

    Potência_Líquida = (potencia_expansor - potencia_compressor) * rendimento
    Q_fornecido = fluxo_compressor * (h3 - h2)
    eficiência_Termica = Potência_Líquida / (Fluxo_massico_combustão*PCI_do_gás_natural)
    return np.array([
        Potência_Líquida/1000,
        eficiência_Termica*100,
        t4-273
    ])

def printSI(Fabricante, resposta):
    Diferença = [100*(resposta[0]-Fabricante[0])/Fabricante[0],100*(resposta[1]-Fabricante[1])/Fabricante[1],100*(resposta[2]-Fabricante[2])/Fabricante[2]]

    # print(f"Potência Líquida {Potência_Líquida}")
    # print(f"Eficiência (%): {eficiência_Termica*100}")
    # print(f"Tgases (C): {t4-273}")
    # print()

    print(f"Fabricante: {Fabricante}")
    print(f"Simulação: {resposta}")
    print(f"Diferença: {Diferença}")

main()
