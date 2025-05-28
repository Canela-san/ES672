import CoolProp.CoolProp as CP


def main():
    Patm = 101325
    fluxo_compressor = 14.16
    relação_pressões_compressão = 10.7
    perda_carga_ar_combustão = 1.5
    PCI_do_gás_natural = 50.01 * 1000000
    temperatura_máxima_do_ciclo = 1078 + 273.15
    perda_de_carga_na_exaustão = 30
    eficiência_isentrópica_compressor = 0.828
    eficiência_isentrópica_expansão = 0.857
    rendimento_eletro_mecânico = 0.975
    resposta = pp02A(Patm,
        fluxo_compressor,
        relação_pressões_compressão,
        perda_carga_ar_combustão,
        PCI_do_gás_natural,
        temperatura_máxima_do_ciclo,
        perda_de_carga_na_exaustão,
        eficiência_isentrópica_compressor,
        eficiência_isentrópica_expansão,
        rendimento_eletro_mecânico)
    print(resposta)



def pp02A(Patm,
        fluxo_compressor,
        relação_pressões_compressão,
        perda_carga_ar_combustão,
        PCI_do_gás_natural,
        temperatura_máxima_do_ciclo,
        perda_de_carga_na_exaustão,
        eficiência_isentrópica_compressor,
        eficiência_isentrópica_expansão,
        rendimento_eletro_mecânico):

    t1 = 15 + 273.15
    p1 = Patm

    # compressor

    pressão_compressor = p1 * relação_pressões_compressão
    h1 = CP.PropsSI('H', 'T', t1, 'P', p1, 'Air')

    s1 = CP.PropsSI('S', 'T', t1, 'P', p1, 'Air')

    s2 = s1
    p2 = p1 * relação_pressões_compressão
    h2s = CP.PropsSI('H', 'S', s2, 'P', p2, 'Air')
    h2 = ((h2s - h1) / eficiência_isentrópica_compressor) + h1
    t2 = CP.PropsSI('T', 'P', p2, 'H', h2, 'Air')
    potencia_compressor = fluxo_compressor * (h2 - h1)

    #camara de combustão
    p3 = (1-(perda_carga_ar_combustão/100))*pressão_compressor
    # h3 = (1.19335*temperatura_máxima_do_ciclo-155.437)*1000
    h3 = CP.PropsSI('H', 'P', p3, 'T', temperatura_máxima_do_ciclo, 'Air')
    Fluxo_massico_combustão=(fluxo_compressor*(h3-h2))/(PCI_do_gás_natural-(h3-h2))
    s3 = CP.PropsSI('S', 'P', p3, 'H', h3, 'Air')

    # p4 = ((1*100)+0.1*perda_de_carga_na_exaustão)*1000
    p4 = p1 + (perda_de_carga_na_exaustão * 100)
    h4s = CP.PropsSI('H', 'S', s3, 'P', p4, 'Air')
    h4 = h3-(eficiência_isentrópica_expansão*(h3-h4s))
    # t4 = 842.9552
    t4 = CP.PropsSI('T', 'H', h4, 'P', p4, 'Air')
    potencia_expansor = (fluxo_compressor+Fluxo_massico_combustão)*(h3-h4)
    # ((h4s-h3)/e)+h3
    # h3-(e*(h3-h4s))
    #Conclusão

    Potência_Líquida = (potencia_expansor - potencia_compressor) * rendimento_eletro_mecânico
    Q_fornecido = fluxo_compressor * (h3 - h2)
    eficiência_Termica = Potência_Líquida / (Fluxo_massico_combustão*PCI_do_gás_natural)

    print(f"Potência Líquida {Potência_Líquida}")
    print(f"Eficiência (%): {eficiência_Termica*100}")
    print(f"Tgases (C): {t4-273}")
    print()

    Fabricante = [3644,29.56,559]
    resposta = [Potência_Líquida/1000, eficiência_Termica*100, t4-273]
    Diferença = [100*(resposta[0]-Fabricante[0])/Fabricante[0],100*(resposta[1]-Fabricante[1])/Fabricante[1],100*(resposta[2]-Fabricante[2])/Fabricante[2]]

    


    print(f"Fabricante: {Fabricante}")
    print(f"Simulação: {resposta}")
    print(f"Diferença: {Diferença}")


    return resposta

main()