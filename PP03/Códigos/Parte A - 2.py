# --- Dados do Problema e Constantes ---

# Propriedades do Ar
m_dot_ar = 1.44 / 60  # kg/s, convertido de kg/min 
T_ar_in = 104  # °C, temperatura de saída do 1º estágio 
T_ar_out = 33  # °C, temperatura de entrada do 2º estágio 
cp_ar = 1.005  # kJ/kg·K, calor específico do ar

# Propriedades da Água
delta_T_agua = 10  # °C, aumento máximo de temperatura permitido 
cp_agua = 4.186  # kJ/kg·K, calor específico da água

# --- Cálculo ---

# Balanço de energia: Calor perdido pelo ar = Calor ganho pela água
# m_ar * cp_ar * (T_ar_in - T_ar_out) = m_agua * cp_agua * delta_T_agua
# Resolvendo para m_agua:
m_dot_agua = (m_dot_ar * cp_ar * (T_ar_in - T_ar_out)) / (cp_agua * delta_T_agua)

# --- Apresentação do Resultado ---

print("--- Cálculo do Fluxo Mássico de Água ---")
print(f"Fluxo mássico de ar: {m_dot_ar:.3f} kg/s")
print(f"Calor perdido pelo ar: {m_dot_ar * cp_ar * (T_ar_in - T_ar_out):.2f} kW")
print("\n--- Resultado ---")
print(f"O fluxo mássico de água requerido é: {m_dot_agua:.4f} kg/s")