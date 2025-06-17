import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import zero_Celsius
from scipy.optimize import minimize
from Modelo_Turbina_ASE50 import *
from Dados_Iniciais import *  # isso deve definir `params_ajuste` e `propriedades_fixas`

# Vetor de resposta desejado
vetor_alvo = np.array(Fabricante)

def main():
    # Extrai chaves e valores iniciais dos parâmetros que serão ajustados
    chaves_ajuste = list(params_ajuste.keys())
    valores_iniciais = np.array([params_ajuste[k] for k in chaves_ajuste])

    # Define limites para cada parâmetro
    bounds = []
    for chave in chaves_ajuste:
        if 'eficiencia' in chave or 'eta' in chave or 'rendimento' in chave:
            bounds.append((0.5, 1.0))  # Exemplo para eficiência
        elif 'T_' in chave:
            bounds.append((273, 2000))  # Exemplo para temperatura
        else:
            bounds.append((1e-6, 1e6))  # Limites genéricos

    # Função custo que recebe vetor de parâmetros e retorna erro
    def custo_vetor(parametros_otimizados):
        novos_params = dict(zip(chaves_ajuste, parametros_otimizados))
        return calc_custo(novos_params, propriedades_fixas)

    # Otimização
    resultado = minimize(custo_vetor, valores_iniciais, bounds=bounds)

    # Resultado final
    params_otimizados = dict(zip(chaves_ajuste, resultado.x))
    resposta_final = Modelo_Turbina_ASE50(**propriedades_fixas, **params_otimizados)

    print("\nParâmetros otimizados:")
    for k, v in params_otimizados.items():
        print(f"{k}: {v}")
    print (params_otimizados)
    print("\nResposta do modelo:")
    print(resposta_final)
    
    print(f"Aqui a diferença: {(resposta_final - vetor_alvo)*100/vetor_alvo}")

    print("\nErro final:")
    print(resultado.fun)

    return 0

def calc_custo(params_ajuste, propriedades_fixas):
    try:
        resposta = np.array(Modelo_Turbina_ASE50(**propriedades_fixas, **params_ajuste))
        return np.sum((resposta - vetor_alvo)**2)
    except Exception as e:
        print("Erro ao calcular custo:", e)
        return 1e9  # Penaliza erro com um custo muito alto

if __name__ == "__main__":
    main()
