import CoolProp.CoolProp as cp
from scipy.optimize import _minimize

# ----- Valores -----
# Empuxo em cruzeiro
# Consumo de combustivel
# Consumo de combustivel em cruzeiro

# ----- Parâmetros Datasheet -----

m_ar_to_pw = 81.65 # kg/s
pressure_ratio_pw = 12.5 
thrust_to_pw = 53.5 # kN
thrust_cruise_pw = 15.8 # kN
spec_fuel_to_pw = 22.2 # (g/s)/kN
spec_fuel_cruise_pw = 25.7 # (g/s)kN
t_max_pw = 1063.15 # K

# ----- Definições -----

t_amb, p_amb, m_ar_iso, v_ar_iso = 230, 31200, 81.65, 0.816

def v(t_amb, p_amb):   # Validado
    return 287 * t_amb / p_amb

def v_exaustao(h4, h5):
    return (2 * (h4 - h5)) ** 0.5

def m_ar_in(m_ar_ISO, v_ar_ISO, v):   # Validado
    return m_ar_ISO * v_ar_ISO / v

def m_comb(m_ar_in, h3, h2, pci):   # validado (mais ou menos)
    return (m_ar_in * (h3 - h2))/(pci - h3)

def spec_m_comb(m_comb, f_empuxo):
    return (m_comb * 1000)/(f_empuxo/1000)

def f_empuxo(m_ar_in, m_comb, v_exaustao, v_in):
    return ((m_ar_in + m_comb) * v_exaustao) - (m_ar_in * v_in) # V_in = 260 m/s em cruzeiro

def calcula_erro_empuxo(press_ratio, eff_isoent_comp, perda_carga_comb, t_max, eff_isoent_turb):

    t1, p1 = 263.7, 50390
    h1 = cp.PropsSI('H', 'T', t1, 'P', p1, 'Air')

    print(f'H1 = {h1}')
    print('--------------')

    s2s = cp.PropsSI('S', 'T', t1, 'P', p1, 'Air')   # s2s = s1
    p2s = press_ratio * p1                           
    h2s = cp.PropsSI('H', 'S', s2s, 'P', p2s, 'Air')

    print(f'S2S = {s2s}, P2S = {p2s}, H2S = {h2s}')
    print('--------------')

    h2 = (h1 + (h2s - h1))/eff_isoent_comp
    p2 = p2s

    print(f'H2 = {h2}, P2 = {p2}')
    print('--------------')

    p3 = p2 * (1 - perda_carga_comb)
    t3 = t_max
    h3 = cp.PropsSI('H', 'P', p3, 'T', t3, 'Air')
    s3 = cp.PropsSI('S', 'P', p3, 'T', t3, 'Air')

    print(f'p3 = {p3}, t3 = {t3}, h3 = {h3}, s3 = {s3}')
    print('--------------')

    s4s = s3
    p4s = p1
    h4s = cp.PropsSI('H', 'S', s4s, 'P', p4s, 'Air')

    print(f's4s = {s3}, p4s = {p4s}, h4s = {h4s}')
    print('--------------')

    h4 = h3-(eff_isoent_turb*(h3-h4s))
    p4 = p4s
    s4 = cp.PropsSI('S', 'H', h4, 'P', p4, 'Air')

    print(f'h4 = {h4}, p4 = {p4}, s4 = {s4}')

    p5 = p_amb
    s5 = s4   # Partindo do pressuposto de que o bocal é isoentrópico (outra forma de fazer?)
    h5 = cp.PropsSI('H', 'P', p5, 'S', s5, 'Air')

    print(f'p5 = {p5}, s5 = {s5}, h5 = {h5}')
    print('--------------')

    v_cruise = v(t_amb, p_amb)
    m_ar_in_cruise = m_ar_in(m_ar_iso, v_ar_iso, v_cruise)
    m_comb_cruise = m_comb(m_ar_in_cruise, h3, h2, 42800000) 
    v_exaustao_cruise = v_exaustao(h4, h5)                # Bug --> numero complexo

    print(f'v_cruise = {v_cruise}')
    print(f'm_ar_in_cruise = {m_ar_in_cruise}')
    print(f'm_comb = {m_comb_cruise}')
    print(f'v_exaustao_cruise = {v_exaustao_cruise}')
    print('--------------')

    return f_empuxo(m_ar_in_cruise, m_comb_cruise, v_exaustao_cruise, 260) 

# ----- Outputs -----

emp = calcula_erro_empuxo(12.5, 0.87, 0.025, t_max_pw, 0.87)
print(emp)

# Determinei o estado 3. Agora preciso descobrir como determinar o 4. Já tenho s4s.


            






