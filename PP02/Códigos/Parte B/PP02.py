import numpy as np
from scipy.optimize import minimize

# ----- Parâmetros Datasheet -----

m_ar_to_pw = 81.65 # kg/s
pressure_ratio_pw = 12.5 
thrust_to_pw = 53.5 # kN
thrust_cruise_pw = 15800 # N
spec_fuel_to_pw = 22.2 # (g/s)/kN
spec_fuel_cruise_pw = 25.7 # (g/s)kN
fuel_cruise_pw = 0.406 # kg/s
t_max_pw = 1063.15 # K

# ----- Definições -----

t_amb, p_amb, m_ar_iso, v_ar_iso = 230, 31200, 81.65, 0.816

params_ajuste = {
    'perda_carga_comb': 0.025,
    't_max': 1063.15,
    'eff_isoent_comp': 0.87,
    'eff_isoent_turb': 0.87,
    'eff_isoent_diff_boc': 1 
}

bounds = [
    (0.02375, 0.2625),        # perda_carga_comb, variação de 5%
    (1009.9925, 1116.3075),   # t_max, variação de 5%
    (0.8265, 0.9135),         # eff_isoent_comp, variação de 5%
    (0.8265, 0.9135),         # eff_isoent_turb, variação de 5%
    (0.95, 1)                 # eff_isoent_diff_boc, variação de 5%
]

inputs_iniciais = list(params_ajuste.values())

def v(t_amb, p_amb):   
    return 287 * t_amb / p_amb

def v_exaustao(h4, h5):
    return (2 * (h4 - h5)) ** 0.5

def m_ar_in(m_ar_ISO, v_ar_ISO, v):   
    return m_ar_ISO * v_ar_ISO / v

def m_comb(m_ar_in, h3, h2, pci):   
    return (m_ar_in * (h3 - h2))/(pci - h3)

def spec_m_comb(m_comb, f_empuxo):
    return (m_comb * 1000)/(f_empuxo/1000)

def f_empuxo(m_ar_in, m_comb, v_exaustao, v_in):
    return ((m_ar_in + m_comb) * v_exaustao) - (m_ar_in * v_in) 

def calcula_erros_individuais(inputs):

    v_cruise = v(t_amb, p_amb)
    m_ar_in_cruise = m_ar_in(m_ar_iso, v_ar_iso, v_cruise)

    h1 = 263820 # J/kg
    h2s = 543750 # J /kg
    h2 = h1 + (h2s - h1)/inputs[2] # J/kg
    h3 = (1.150*inputs[1] - 104.05)*1000 # J/kg

    m_comb_cruise = m_comb(m_ar_in_cruise, h3, h2, 42800000) 

    h4s = h3 - ((m_ar_in_cruise*(h2 - h1))/((m_ar_in_cruise + m_comb_cruise)*inputs[3]))
    h4 = h3 - inputs[3]*(h3 - h4s)
    h5s = 518600
    h5 = h4 - inputs[4]*(h4-h5s)

    v_exaustao_cruise = v_exaustao(h4, h5)               
    empuxo = f_empuxo(m_ar_in_cruise, m_comb_cruise, v_exaustao_cruise, 260) 
    m_comb_cruise_spec = (m_comb_cruise*1000)/(empuxo/1000)

    erros = [
        (empuxo - thrust_cruise_pw)/thrust_cruise_pw, 
        (m_comb_cruise - fuel_cruise_pw)/fuel_cruise_pw, 
        (m_comb_cruise_spec - spec_fuel_cruise_pw)/spec_fuel_cruise_pw
    ]

    return erros

def calcula_erro_combinado(inputs):

    v_cruise = v(t_amb, p_amb)
    m_ar_in_cruise = m_ar_in(m_ar_iso, v_ar_iso, v_cruise)

    h1 = 263820 # J/kg
    h2s = 543750 # J /kg
    h2 = h1 + (h2s - h1)/inputs[2] # J/kg
    h3 = (1.150*inputs[1] - 104.05)*1000 # J/kg

    m_comb_cruise = m_comb(m_ar_in_cruise, h3, h2, 42800000) 

    h4s = h3 - ((m_ar_in_cruise*(h2 - h1))/((m_ar_in_cruise + m_comb_cruise)*inputs[3]))
    h4 = h3 - inputs[3]*(h3 - h4s)
    h5s = 518600
    h5 = h4 - inputs[4]*(h4-h5s)

    v_exaustao_cruise = v_exaustao(h4, h5)               
    empuxo = f_empuxo(m_ar_in_cruise, m_comb_cruise, v_exaustao_cruise, 260) 
    m_comb_cruise_spec = (m_comb_cruise*1000)/(empuxo/1000)

    erro = ((empuxo - thrust_cruise_pw)**2 + (m_comb_cruise - fuel_cruise_pw)**2 + (m_comb_cruise_spec - spec_fuel_cruise_pw)**2)**0.5

    return erro

def main():

    resultado = minimize(calcula_erro_combinado, inputs_iniciais, bounds=bounds)
    
    if resultado.success:
        parametros_otimos = resultado.x
        erros = calcula_erros_individuais(parametros_otimos)

        print(f'Erro empuxo = {erros[0]}')
        print(f'Erro consumo de comb. = {erros[1]}')
        print(f'Erro consumo esp. de comb. = {erros[2]}')
    else:
        print('A otimização falhou. Mensagem:')
        print(resultado.message)


            






