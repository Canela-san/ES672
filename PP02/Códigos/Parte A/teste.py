import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import zero_Celsius
from Modelo_Turbina_ASE50 import *
from Dados_Iniciais import *




# params_ajuste = {'perda_carga_ar_combustão': np.float64(1.4637794450670145), 'T_max': np.float64(1365.838519043944), 'eta_comp': np.float64(0.8446615021146631), 'eta_turb': np.float64(0.8887808893664478), 'rendimento_mecânico': np.float64(0.8666943779345587), 'perda_exaustao': np.float64(29.277409918315872)}
resposta = Modelo_Turbina_ASE50(**propriedades_fixas, **params_ajuste)
print(resposta)
print(Fabricante)
print([resposta[0] - Fabricante[0],resposta[1] - Fabricante[1],resposta[2] - Fabricante[2]])
