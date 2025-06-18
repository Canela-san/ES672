import CoolProp.CoolProp as CP
from scipy.constants import zero_Celsius

import math

# --- Dados Fornecidos ---

# Constantes e conversões
R_ar = 0.287  # kJ/kg·K
m_dot_kg_min = 1.44  # kg/min
m_dot_kg_s = m_dot_kg_min / 60  # kg/s

# Estágio 1 (Baixa Pressão)
P1 = 91.4  # kPa
T1_C = 30  # °C
P2 = 400  # kPa
T2_C = 104  # °C

# Estágio 2 (Alta Pressão)
P3 = 400  # kPa
T3_C = 33  # °C
P4 = 800  # kPa
T4_C = 70  # °C

# Conversão de temperaturas para Kelvin
T1_K = T1_C + 273.15
T2_K = T2_C + 273.15
T3_K = T3_C + 273.15
T4_K = T4_C + 273.15

# --- Passo 1: Cálculos do Primeiro Estágio ---

# Calcular o expoente politrópico n1
# (T2/T1) = (P2/P1)^((n1-1)/n1)
# ln(T2/T1) = ((n1-1)/n1) * ln(P2/P1)
# (n1-1)/n1 = ln(T2/T1) / ln(P2/P1)
fator_n1 = math.log(T2_K / T1_K) / math.log(P2 / P1)
n1 = 1 / (1 - fator_n1)

# Calcular a potência do primeiro estágio (W1)
# W1 = m_dot * (n1 * R / (n1-1)) * (T2 - T1)
W1 = m_dot_kg_s * (n1 * R_ar / (n1 - 1)) * (T2_K - T1_K)

# --- Passo 2: Cálculos do Segundo Estágio ---

# Calcular o expoente politrópico n2
# (T4/T3) = (P4/P3)^((n2-1)/n2)
fator_n2 = math.log(T4_K / T3_K) / math.log(P4 / P3)
n2 = 1 / (1 - fator_n2)

# Calcular a potência do segundo estágio (W2)
# W2 = m_dot * (n2 * R / (n2-1)) * (T4 - T3)
W2 = m_dot_kg_s * (n2 * R_ar / (n2 - 1)) * (T4_K - T3_K)

# --- Passo 3: Cálculo da Potência Total ---

W_total = W1 + W2

# --- Apresentação dos Resultados ---

print("--- Análise da Compressão em Dois Estágios ---")
print(f"Fluxo mássico: {m_dot_kg_s:.3f} kg/s")
print("\n--- Primeiro Estágio ---")
print(f"Expoente politrópico (n1): {n1:.3f}")
print(f"Potência requerida (W1): {W1:.5f} kW")
print("\n--- Segundo Estágio ---")
print(f"Expoente politrópico (n2): {n2:.3f}")
print(f"Potência requerida (W2): {W2:.5f} kW")
print("\n--- Potência Total ---")
print(f"Potência total requerida (W_total): {W_total:.5f} kW")