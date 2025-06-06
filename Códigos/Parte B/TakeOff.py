import CoolProp.CoolProp as cp

t_amb, p_amb = 288.15, 101325 # K, Pa

m_ar_iso, v_ar_iso = 81.65, 0.816

inputs = [0.025, 1068.23, 0.866, 0.87, 0.987]

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

def calcula_to(inputs):

    h_amb = cp.PropsSI('H', 'T', t_amb, 'P', p_amb, 'Air')   

    h1 = h_amb + ((62**2)/2)   
    p1 = 1.61 * p_amb
    s1 = cp.PropsSI('S', 'H', h1, 'P', p1, 'Air')

    s2s = s1
    p2s = 12.5 * p1
    h2s = cp.PropsSI('H', 'S', s2s, 'P', p2s, 'Air')

    h2 = h1 + (h2s-h1)/inputs[2]
    p2 = p2s

    p3 = p2 * (1 - inputs[0])
    t3 = inputs[1]
    h3 = cp.PropsSI('H', 'P', p3, 'T', t3, 'Air')
    s3 = cp.PropsSI('S', 'P', p3, 'H', h3, 'Air')

    s4s = s3
    p4s = p1
    h4s = cp.PropsSI('H', 'S', s4s, 'P', p4s, 'Air')
    
    h4 = h3 - inputs[3]*(h3 - h4s)
    p4 = p4s
    s4 = cp.PropsSI('S', 'H', h4, 'P', p4, 'Air')

    p5 = p_amb
    s5 = s4
    h5 = cp.PropsSI('H', 'P', p5, 'S', s5, 'Air')
    
    v_to = v(t_amb, p_amb)
    m_ar_in_to = m_ar_in(m_ar_iso, v_ar_iso, v_to)
    v_exaustao_to = v_exaustao(h4, h5)
    m_comb_to = m_comb(m_ar_in_to, h3, h2, 42800000)
    emp_to = f_empuxo(m_ar_in_to, m_comb_to, v_exaustao_to, 62)
    m_comb_to_spec = (m_comb_to*1000)/(emp_to/1000)

    print(f'v = {v_to}, m_in = {m_ar_in_to}, v_ex = {v_exaustao_to}, m_comb = {m_comb_to}, m_spec = {m_comb_to_spec}, emp = {emp_to}')

    print(f'Emp = {emp_to}')
    print(f'm_comb = {m_comb_to}')
    print(f'm_comb_spec = {m_comb_to_spec}')

    print(h_amb, h1, h2, h3, h4, h5)

calcula_to(inputs)
