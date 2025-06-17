import math

# --- Constantes e Dados Iniciais ---

# Constante do gás para o ar (kJ/kg.K)
R_air = 0.287

# Dados do compressor de dois estágios (Tabela 1)
P1 = 91.4  # Pressão de entrada (kPa) 
T1_C = 30    # Temperatura de entrada (°C) 
P2 = 400   # Pressão intermediária (kPa) 
T2_C = 104   # Temperatura saída estágio 1 (°C) 
T3_C = 33    # Temperatura entrada estágio 2 (°C) 
P4 = 800   # Pressão de descarga (kPa) 
T4_C = 70    # Temperatura de descarga (°C) 

# Fluxos mássicos (Tabela 2)
m_dot_2s_kg_min = 1.44  # Compressor de 2 estágios (kg/min) 
m_dot_1s_kg_min = 1.16  # Compressor de 1 estágio (kg/min) 

# --- Conversões de Unidades ---

# Temperaturas de Celsius para Kelvin
T1_K = T1_C + 273.15
T2_K = T2_C + 273.15
T3_K = T3_C + 273.15
T4_K = T4_C + 273.15

# Fluxos mássicos de kg/min para kg/s
m_dot_2s_kg_s = m_dot_2s_kg_min / 60
m_dot_1s_kg_s = m_dot_1s_kg_min / 60

# --- Análise do Compressor de Dois Estágios ---

print("--- Análise do Compressor de Dois Estágios ---")

# 1. Calcular expoentes politrópicos (n) para cada estágio
# (n-1)/n = ln(T_out/T_in) / ln(P_out/P_in)
# n = 1 / (1 - (ln(T_out/T_in) / ln(P_out/P_in)))
n_ratio_1 = math.log(T2_K / T1_K) / math.log(P2 / P1)
n1 = 1 / (1 - n_ratio_1)

n_ratio_2 = math.log(T4_K / T3_K) / math.log(P4 / P2)
n2 = 1 / (1 - n_ratio_2)

print(f"Expoente politrópico do estágio 1 (n1): {n1:.4f}")
print(f"Expoente politrópico do estágio 2 (n2): {n2:.4f}")

# 2. Calcular a potência (trabalho) para cada estágio
# W_dot = m_dot * (n*R / (n-1)) * (T_out - T_in)
W_dot_stage1 = m_dot_2s_kg_s * (n1 * R_air / (n1 - 1)) * (T2_K - T1_K)
W_dot_stage2 = m_dot_2s_kg_s * (n2 * R_air / (n2 - 1)) * (T4_K - T3_K)
W_dot_total_2s = W_dot_stage1 + W_dot_stage2

print(f"Potência do estágio 1: {W_dot_stage1:.2f} kW")
print(f"Potência do estágio 2: {W_dot_stage2:.2f} kW")
print(f"Potência total requerida: {W_dot_total_2s:.2f} kW")

# 3. Calcular consumo de eletricidade e massa em 1 hora
energy_2s_kwh = W_dot_total_2s * 1  # Energia em kWh para 1h de operação
mass_2s_kg = m_dot_2s_kg_min * 60

print(f"\nConsumo de eletricidade em 1 hora: {energy_2s_kwh:.2f} kWh")
print(f"Massa de gás comprimido em 1 hora: {mass_2s_kg:.1f} kg\n")


# --- Análise do Compressor de Um Estágio ---

print("--- Análise do Compressor de Um Estágio ---")

# 1. Usar n1 como expoente, conforme instruído 
n_1s = n1

# 2. Calcular a temperatura de saída
# T_out = T_in * (P_out/P_in)^((n-1)/n)
T_out_1s_K = T1_K * (P4 / P1)**n_ratio_1
T_out_1s_C = T_out_1s_K - 273.15

print(f"Usando n = {n_1s:.4f}, a temperatura de saída seria: {T_out_1s_C:.1f} °C")

# 3. Calcular a potência total
W_dot_total_1s = m_dot_1s_kg_s * (n_1s * R_air / (n_1s - 1)) * (T_out_1s_K - T1_K)
print(f"Potência total requerida: {W_dot_total_1s:.2f} kW")

# 4. Calcular consumo de eletricidade e massa em 1 hora
energy_1s_kwh = W_dot_total_1s * 1 # Energia em kWh para 1h de operação
mass_1s_kg = m_dot_1s_kg_min * 60

print(f"\nConsumo de eletricidade em 1 hora: {energy_1s_kwh:.2f} kWh")
print(f"Massa de gás comprimido em 1 hora: {mass_1s_kg:.1f} kg")