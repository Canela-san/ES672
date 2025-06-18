import math

# --- Dados do Problema e Constantes ---

# Dados para o compressor de estágio único
m_dot_1_stage = 1.16 / 60  # kg/s, da Tabela 2
P_in = 91.4  # kPa
T_in_C = 30  # °C
P_out = 800  # kPa

# Constantes e valores da análise anterior
n = 1.1736  # Expoente politrópico do 1º estágio da compressão estagiada
R_ar = 0.287  # kJ/kg·K, constante do ar
T_in_K = T_in_C + 273.15 # Temperatura de entrada em Kelvin


# --- Cálculo ---

# 1. Calcular a temperatura de saída (Tout)
fator_n = (n - 1) / n
T_out_K = T_in_K * math.pow((P_out / P_in), fator_n)
T_out_C = T_out_K - 273.15

# 2. Calcular a potência requerida (W)
W_1_stage = m_dot_1_stage * (n * R_ar / (n - 1)) * (T_out_K - T_in_K)


# --- Apresentação dos Resultados ---

print("--- Análise do Compressor de Estágio Único ---")
print(f"Fluxo mássico: {m_dot_1_stage:.4f} kg/s")
print(f"Expoente politrópico (n): {n:.3f}")
print(f"\nTemperatura de saída calculada: {T_out_K:.1f} K ({T_out_C:.1f} °C)")
print(f"Potência requerida (W): {W_1_stage:.2f} kW")