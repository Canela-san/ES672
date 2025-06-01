import CoolProp.CoolProp as CP
from scipy.constants import zero_Celsius
def pp02A(
        Patm,
        fluxo_compressor,
        relação_pressões_compressão,
        perda_carga_ar_combustão,
        PCI_do_gás_natural,
        T_max,
        perda_exaustao,
        eta_comp,
        eta_turb,
        rendimento_mecânico,
        T_ambiente
        ):

    t1 = T_ambiente + zero_Celsius
    p1 = Patm

    # compressor

    pressão_compressor = p1 * relação_pressões_compressão
    h1 = CP.PropsSI('H', 'T', t1, 'P', p1, 'Air')
    s1 = CP.PropsSI('S', 'T', t1, 'P', p1, 'Air')

    s2 = s1
    p2 = p1 * relação_pressões_compressão
    h2s = CP.PropsSI('H', 'S', s2, 'P', p2, 'Air')
    h2 = ((h2s - h1) / eta_comp) + h1
    # t2 = CP.PropsSI('T', 'P', p2, 'H', h2, 'Air')    #Não é usado
    potencia_compressor = fluxo_compressor * (h2 - h1)

    #camara de combustão

    p3 = (1-(perda_carga_ar_combustão/100))*pressão_compressor
    h3 = CP.PropsSI('H', 'P', p3, 'T', T_max, 'Air')
    Fluxo_massico_combustão=(fluxo_compressor*(h3-h2))/(PCI_do_gás_natural-(h3-h2))
    s3 = CP.PropsSI('S', 'P', p3, 'H', h3, 'Air')

    #Exaustão
    p4 = p1 + (perda_exaustao * 100)
    h4s = CP.PropsSI('H', 'S', s3, 'P', p4, 'Air')
    h4 = h3-(eta_turb*(h3-h4s))
    t4 = CP.PropsSI('T', 'H', h4, 'P', p4, 'Air')
    potencia_expansor = (fluxo_compressor+Fluxo_massico_combustão)*(h3-h4)

    #Conclusão

    Potência_Líquida = (potencia_expansor - potencia_compressor) * rendimento_mecânico
    # Q_fornecido = fluxo_compressor * (h3 - h2)   # Não é usado
    eficiência_Termica = Potência_Líquida / (Fluxo_massico_combustão*PCI_do_gás_natural)
    return [
        Potência_Líquida/1000,
        eficiência_Termica*100,
        t4-zero_Celsius
    ]
