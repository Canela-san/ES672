    
from scipy.constants import zero_Celsius



Fabricante= [3644,29.56,559]

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

    # Nome amigável para cada função
param_names = {
        'perda_carga_ar_combustao': 'Perda carga ar combustão',
        'T_max': 'Temperatura Máxima',
        'eta_comp': 'Eficiência Isentrópica Compressor',
        'eta_turb': 'Eficiência Isentrópica Expansão',
        'rendimento_mecânico': 'Rendimento Eletromecânico',
        'perda_exaustao': 'Perda de carga na exaustão'
}
param_names_v = list(param_names.values())

legenda = [
        ['Variação Percentual (%)','Potência Líquida (kW)','Potencia Líquida x Variação de Parâmetros'],
        ['Variação Percentual (%)','Eficiência Térmica','Eficiência Térmica x Variação de Parâmetros'],
        ['Variação Percentual (%)','Temperatura do Gás de Exaustão (C)','Temperatura do Gás de Exaustão x Variação de Parâmetros']  
]
