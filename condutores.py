<<<<<<< HEAD
import pandas as pd
import numpy as np
from leituras import Leitura

leitura = Leitura() 
tab421 = leitura.tabela(sheet_name = "4.21")
tab421 = tab421.replace({'Cabo isolado em XLPE':'XLPE', 'Cabo isolado em EPR':'EPR'})
tab42 = leitura.tabela(sheet_name = "4.2")
tab46 = leitura.tabela(sheet_name = "4.6")
tab47 = leitura.tabela(sheet_name = "4.7")
tab48 = leitura.tabela(sheet_name = "4.8")
tab49 = leitura.tabela(sheet_name = "4.9")

class Condutor():
    """Parâmetros: 
            material_isolante : string
                Uma string que informa o tipo do material isolante: XLPE, EPR.

            tipo_condutor : string
                Uma string que informa o material do condutor: "Fio de alumínio duro"; 
                    "Fio de cobre duro"; "IACS – padrão internacional de cobre recozido"; 
                    "Zincado para alma de cabos de alumínio".

            fator_secao_tensao : string ou numero
                Um número para a seção do condutor, para a classe de tensão "8.7kV - 15kV";
                    para classes de tensão diferentes, inserir o número para a seção do condutor + ".1", ex: "300.1"."""
    def __init__(self, material_isolante, tipo_condutor, fator_secao_tensao, fator_diametro, tensao_linha):

        self.material_isolante = material_isolante
        self.tipo_condutor = tipo_condutor
        self.fator_secao_tensao = fator_secao_tensao
        self.fator_diametro = fator_diametro
        self.tensao_fase = tensao_linha / np.sqrt(3)

    def gradiente_potencial(self, e_is, e_imp, tensao_fase, B, Rc, A):
        """Calcula o gradiente de potencial a que fica submetido um vazio ou uma impureza qualquer no interior da isolação [kV/mm].
        
            Parâmetros:
                e_is : número
                    Constante dielétrica do material isolante.

                e_imp : número
                    Constante dielétrica do material que constitui a impureza.

                tensao_fase : número
                    Tensão de fase [kV].

                B : número
                    Distância entre o ponto considerado no interior da isolação e a superfície do condutor [mm].

                Rc : número
                    Raio do condutor [mm].

                A : número
                    Espessura da camada isolante [mm]."""

        # Variável que armazena o valor do gradiente de potencial
        Vb = (0.869 * (e_is / e_imp) * self.tensao_fase) / ((B + Rc) * np.log((Rc + A) / Rc))

        return Vb

    def raio_condutor(self):
        """Retorna o raio do condutor (Rc) [mm]."""
        
        # Variável que armazena o valor do raio do condutor após buscar na tabela
        Rc = (1/2) * tab421.loc[tab421['Tipo de isolação'] == self.material_isolante].loc[tab421['Caracteristica']
                                                                                    == 'Diâmetro do condutor - mm', [self.fator_secao_tensao]].values[0,0]
        return Rc

    def distancia_B(self):
        """Retorna a distância entre o ponto considerado no interior da isolação e a superfície do condutor (B) [mm]."""

        # Variável que armazena da distância B após buscar na tabela
        B = (1/2) * tab421.loc[tab421['Tipo de isolação'] == self.material_isolante].loc[tab421['Caracteristica']
                                                                                    == 'Espessura da isolação -mm', [self.fator_secao_tensao]].values[0,0]
        return B

    def espessura_camada_isolante(self):
        """Retorna a espessura da camada isolante (A) [mm]."""

        # Variável que armazena o valor da espessura da isolação após buscar na tabela
        A = tab421.loc[tab421['Tipo de isolação'] == self.material_isolante].loc[tab421['Caracteristica']
                                                                            == 'Espessura da isolação -mm', [self.fator_secao_tensao]].values[0,0]

        return A

    def funcao_constante_dieletrica_isolante(self):
        """Retorna a constante dieletrica do material isolante (e_is)."""

        # Variável que armazena o valor da constante dielétrica do material isolante após buscar na tabela
        constante_dieletrica_isolante = tab46.loc[tab46['Materiais Isolantes'] == self.material_isolante, [
            'ε']].values[0,0]

        return constante_dieletrica_isolante

    def funcao_constante_dieletrica_impureza(self, material_impureza):
        """Retorna a constante dielétrica do material que constitui a impureza (e_imp).
        
            Parâmetros:
                material_impureza : string
                    Tipo de material que constitui a isolação.
                    [PVC, XLPE, EPR, Papel impregnado, Papelão isolante impregnado,
                     Papelão endurecido, Óleo isolante, Porcelana, Mica, Ar ou Madeira impregnada]"""

        # Variável que armazena o valor da constante dielétrica da impureza após buscar na tabela
        constante_dieletrica_impureza = tab46.loc[tab46['Materiais Isolantes'] == material_impureza, [
            'ε']].values[0,0]

        return constante_dieletrica_impureza

    def capacitancia_cabo(self, Dc, A, Ebi):
        """Calcula a capacitância do cabo [uF/km].
        
           Parâmetros:
                Dc : número
                    Diâmetro do condutor [mm].

                A : número
                    Espessura da camada isolante [mm].

                Ebi : número
                    Espessura da blindagem interna das fitas semicondutores [mm]."""

        # Variável que armazena o valor do diâmetro sobre a isolação do material isolante
        Dsi = Dc + 2 * A + 2 * Ebi
        # Variável que recebe o valor da constante dielétrica do material
        constante_dieletrica_isolante = self.funcao_constante_dieletrica_isolante()
        # Variável que armazena o valor da capacitância calculada
        C = (0.0556 * constante_dieletrica_isolante) / (np.log(Dsi / (Dc + 2 * Ebi)))

        return C

    def perdas_dieletricas(self, C):
        """Calcula as perdas dielétricas do cabo [W/m].
        
            Parâmetros:
                C : número
                    Capacitância do cabo [uF/km]."""

        tangente_delta = tab46.loc[tab46['Materiais Isolantes']
                                == self.material_isolante, ['tg δ (20ºC)']].values[0,0]

        Pd = 0.3769 * C * (self.tensao_fase**2) * tangente_delta

        return Pd

    def perda_dieletrica_total(self, Pd, comprimento):
        """Calcula as perdas totais dielétricas do cabo [W].
        
            Parâmetros:
                Pd : número
                    Perdas dielétricas do cabo [W/m].
                    
                comprimento: número
                    Comprimento do cabo [m]."""

        Pdt = Pd * comprimento

        return Pdt

    def diametro_externo(self):
        """Retorna o diâmetro externo do cabo [mm]."""

        Dca = tab421.loc[tab421['Tipo de isolação'] == self.material_isolante].loc[tab421['Caracteristica']
                                                                            == 'Diâmetro externo - mm', [self.fator_secao_tensao]].values[0,0]

        return Dca

    def fator_K(self, fator, encordoamento, fator_diametro):
        """Retorna o fator K.
        
            Parâmetros:
                INCOMPLETO"""

        if fator_diametro != 0:
            K = tab47.loc[tab47['Fator'] == fator].loc[tab47['Condutor'] == encordoamento, [fator_diametro]].values[0,0]
        else:
            K = tab47.loc[tab47['Fator'] == fator].loc[tab47['Condutor'] == encordoamento, ['Unnamed: 2']].values[0,0]

        return K

    def resistencia_cc(self, K1, K2, K3, p20, a20, Tc, S):
        """Calcula a resistência em corrente contínua a T°C [mΩ/m].
        
            Parâmetros:
                K1 : número
                    Fator que depende do diâmetro dos fios elementares do condutor e do tipo de encordoamento (Tabela 4.7).

                K2 : número
                    Fator que depende do tipo de encordoamento do condutor (Tabela 4.7).

                K3 : número
                    Fator que depende do tipo de reunião dos cabos componentes do cabo multipolar (Tabela 4.7).

                p20 : número
                    Resistividade do material condutor [Ωmm²/m].
                    
                a20 : número
                    Coeficiente de temperatura do material condutor [1/°C].
                    
                Tc : número
                    Temperatura do condutor [°C] (adotar normalmente a temperatura máxima admitida pela isolação).
                    
                S : número
                    Seção do condutor [mm²]."""

        Rcc = (1/S) * (1000 * K1 * K2 * K3 * p20) * (1 + a20 * (Tc - 20))

        return Rcc

    def componente_correcao_efeito_peculiar(self, Rcc):
        """Calcula a componente que corrige o efeito pelicular da distribuição de corrente na seção do condutor.
        
            Parâmetros:
                Rcc : número
                    Resistência em corrente contínua a T°C [mΩ/m]."""

        Fs = 0.15 / Rcc
        Ys = (Fs**2) / (192 + 0.8 * (Fs**2))

        return Ys

    def componente_correcao_proximidade_cabos(self, Ys, Dc, Dmg):
        """Calcula a componente que corrige o efeito de proximidade entre os cabos.

            Parâmetros:
                Ys : número
                    Componente que corrige o efeito pelicular da distribuição de corrente na seção do condutor.
                    
                Dc : número
                    Diâmetro do condutor [mm].
                    
                Dmg : número
                    Distância média geométrica do conjunto de cabos componentes [mm]."""

        Yp = Ys * ((Dc / Dmg)**2) * ((1.18 / (0.27 + Ys)) + 0.312 * ((Dc / Dmg)**2))

        return Yp

    def calcular_Dmg(self, D):
        """Calcula o diâmetro médio geométrico.

        INCOMPLETO"""

        return 1.26 * D

    def resistividade_condutor(self):
        """Retorna a resistividade máxima do condutor a 20°C [Ω/mm²/m]."""

        resistividade = tab42.loc[tab42['Especificações'] ==
                                'Resistividade máxima a 20ºC (Ω/mm2/m)', [self.tipo_condutor]].values[0,0]

        return resistividade

    def coeficiente_temperatura(self):
        """Retorna o coeficiente de variação da resistência/°C do condutor a 20°C."""

        coeficiente_temperatura = tab42.loc[tab42['Especificações'] ==
                                            'Coeficiente de variação da resistência/ºC a 20ºC', [self.tipo_condutor]].values[0,0]
        return coeficiente_temperatura

    def reatancia_positiva(self, Dmg, Dc):
        """Calcula a reatância indutiva de sequência positiva [mΩ/m].
        
            Parâmetros:
                Dmg : número
                    Distância média geométrica do conjunto de cabos componentes [mm].
                    
                Dc : número
                    Diâmetro do condutor [mm]."""

        Xp = 0.0754 * np.log((Dmg) / (0.779 * (Dc / 2)))

        return Xp

    def reatancia_blindagem(self):
        """Calcula a reatância da blindagem para um ponto de aterramento [mΩ/m].
        
        INCOMPLETO"""

        Dca = self.diametro_externo()
        D = Dca  # teste
        Dmg = self.calcular_Dmg(D)
        Dc = 2 * self.raio_condutor()
        Ei = self.espessura_camada_isolante()
        Ebi = 1 #teste
        Ebe = 1 #teste
        Ebm = 1 #teste
        Dmb = self.diametro_medio_blindagem(Dc, Ei, Ebi, Ebe, Ebm)

        Xb = 0.0754 * np.log((2 * Dmg) / (Dmb))

        return Xb

    def acrescimo_componente_resistivo(self, Rb, Xb):
        """Calcula o acréscimo do componente resistivo da impedância de sequência positiva [mΩ/m].
        
            Parâmetros:
                Rb : número
                    Resistência da blindagem metálica [mΩ/m].
                    
                Xb : número
                    Reatância indutiva da blindagem metálica [mΩ/m]."""

        delta_Rb = Rb / (((Rb / Xb)**2) + 1)

        return delta_Rb

    def resistencia_blindagem(self):
        """Calcula a resistência da blindagem [mΩ/m]."""

        K4 = self.fator_K('K4', 'Fio ou encordoamento compacto', self.fator_diametro)
        resistividade = self.resistividade_condutor()
        coeficiente_temp = self.coeficiente_temperatura()
        Sb = 300#self.secao_blindagem(diametro_fio, intensidade_corrente)
        Tb = 90 #teste
        Rb = (1 + coeficiente_temp * (Tb - 20)) * (1000 * K4 * resistividade) / Sb

        return Rb

    def secao_blindagem(self, diametro_fio, intensidade_corrente):
        """Retorna a seção da blindagem [mm²].

            Parâmetros:
                diametro_fio : número
                    Diâmetro dos fios [mm].
                    
                intensidade_corrente : número
                    Intensidade máxima admitida em curto-circuito (1 s) [kA]."""

        Sb = tab48.loc[tab48['Diâmetro dos fios em mm'] == diametro_fio].loc[tab48['Intensidade máx. adm. em curto-circuito (1s) kA'] == intensidade_corrente, [
            'Seção da blindagem (mm²)']].values[0, 0]

        return Sb

    def reducao_indutancia(self, M, Rb, Xb):
        """Calcula a redução da indutância de sequência positiva [mH/km].
            
            Parâmetros:
                M : número
                    Indutância mútua por fase [mH/km].

                Rb : número
                    Resistência da blindagem metálica [mΩ/m].
                    
                Xb : número
                    Reatância indutiva da blindagem metálica [mΩ/m]."""

        delta_Lb = ((M) / (((Rb / Xb)**2) + 1))

        return delta_Lb

    def reducao_reatancia_positiva(self, Rb, Xb):
        """Calcula a redução da reatância de sequência positiva [Ω/km].
        
            Parâmetros:                
                Rb : número
                    Resistência da blindagem metálica [mΩ/m].
                    
                Xb : número
                    Reatância indutiva da blindagem metálica [mΩ/m]."""

        delta_Xb = ((Xb) / (((Rb / Xb)**2) + 1))

        return delta_Xb

    def acrescimos_resistencia_reatancia_positiva(self):
        """Retorna os valores de acréscimo das componentes resistiva e indutiva (delta_Rb, delta_Xb) [mΩ/m, Ω/km]."""

        Xb = self.reatancia_blindagem()
        Rb = self.resistencia_blindagem()

        delta_Rb = self.acrescimo_componente_resistivo(Rb, Xb)
        delta_Xb = self.reducao_reatancia_positiva(Rb, Xb)

        return delta_Rb, delta_Xb


    def diametro_medio_blindagem(self, Dc, Ei, Ebi, Ebe, Ebm):
        """Calcula o diâmetro médio da blindagem [mm].
        
            Parâmetros:
                Dc : número
                    Diâmetro do condutor [mm].

                Ei : número
                    Espessura da isolação [mm].
                    
                Ebi : número
                    Espessura da blindagem interna das fitas semicondutores, não condutora [mm].
                    
                Ebe : número
                    Espessura da blindagem externa de campo elétrico, não condutora [mm].
                    
                Ebm : número
                    Espessura da blindagem metálica [mm]."""

        Dmb = Dc + 2 * Ei + 2 * Ebi + 2 * Ebe + (Ebm / 2)

        return Dmb

    def resistencia_positiva(self, Dmg, Dc):
        """Calcula a resistência positiva à corrente alternada [mΩ/m].
        
            Parâmetros:
                Dmg : número
                    Distância média geométrica do conjunto de cabos componentes [mm]
                    
                Dc : número
                    Diâmetro do condutor [mm]."""
        
        K1 = self.fator_K('K1', 'Fio ou encordoamento compacto', self.fator_diametro)
        K2 = self.fator_K('K2', 'Fio ou encordoamento compacto', 0)
        K3 = self.fator_K('K3', 'Cabos singelos', 0)
        p20 = self.resistividade_condutor()
        a20 = self.coeficiente_temperatura()
        Tc = 90  # teste
        S = 300
        Rcc = self.resistencia_cc(K1, K2, K3, p20, a20, Tc, S)
        Ys = self.componente_correcao_efeito_peculiar(Rcc)
        Yp = self.componente_correcao_proximidade_cabos(Ys, Dc, Dmg)
        Rp = Rcc * (1 + Ys + Yp)

        return Rp

    def reatancia_positiva_efetiva(self, Xp, delta_Xb):
        """Calcula a reatância positiva efetiva para vários pontos de aterramento [mΩ/m].
        
            Parâmetros:
                Xp : número
                    Reatância indutiva de sequência positiva [mΩ/m].
                    
                delta_Xb : número
                    Componente de redução da reatância de sequência positiva [Ω/km]."""

        Xf = Xp - delta_Xb/10e3

        return Xf

    def resistencia_positiva_efetiva(self, Rp, delta_Rb):
        """Calcula a resistência positiva efetiva para vários pontos de aterramento [mΩ/m].
        
            Parâmetros:
                Rp : número
                    Resistência positiva à corrente alternada [mΩ/m].
                    
                delta_Rb : número
                    Componente de acréscimo resistivo da impedância de sequência positiva [mΩ/m]."""

        Rf = Rp + delta_Rb

        return Rf

    def impedancia_positiva_aterrada_um_ponto(self):
        """Calcula a impedância de sequência positiva para apenas um ponto de aterramento [mΩ/m]."""

        Dc = 2 * self.raio_condutor()
        Dca = self.diametro_externo()
        D = Dca  # teste
        Dmg = self.calcular_Dmg(D)
        Rp = self.resistencia_positiva(Dmg, Dc)
        Xp = self. reatancia_positiva(Dmg, Dc)
        Zp = np.complex(Rp, Xp)

        return Zp

    def impedancia_positiva_aterrada_pontos(self):
        """Calcula a impedância de sequência positiva para vários pontos de aterramento [mΩ/m]."""

        Zp = self.impedancia_positiva_aterrada_um_ponto()
        Rp = np.real(Zp)
        Xp = np.imag(Zp)

        delta_Rb, delta_Xb = self.acrescimos_resistencia_reatancia_positiva()
        Rpf = self.resistencia_positiva_efetiva(Rp, delta_Rb)
        Xpf = self.reatancia_positiva_efetiva(Xp, delta_Xb)
        Zpf = np.complex(Rpf, Xpf)

        return Zpf

    def impedancia_negativa_aterrada_um_ponto(self):
        """Calcula a impedância de sequência negativa para apenas um ponto de aterramento [mΩ/m]."""

        Zn =  self.impedancia_positiva_aterrada_um_ponto()
        
        return Zn

    def impedancia_negativa_aterrada_varios_pontos(self):
        """Calcula a impedância de sequência negativa para vários pontos de aterramento [mΩ/m]."""

        Znf =  self.impedancia_positiva_aterrada_pontos()
        
        return Znf

    def resistencia_circuito_retorno_solo(self, resistividade):
        """Retorna a resistência de circuito de retorno pelo solo [mΩ/m].
        
            Parâmetros:
                resistividade : número
                    Resistividade do solo [Ω/m]."""
        
        Rrs = tab49.loc[tab49['Resistividade do solo (Ω.m) '] == resistividade, ['Resistência do circuito de retorno pelo solo (mΩ/m)']].values[0, 0]

        return Rrs

    def distancia_retorno_solo(self, resistividade):
        """Retorna a distância equivalente para o circuito de retorno [mm].
        
            Parâmetros:
                resistividade : número
                    Resistividade do solo [Ω/m]."""

        Deq = tab49.loc[tab49['Resistividade do solo (Ω.m) '] == resistividade, ['Distância equivalente para o circuito de retorno (mm)']].values[0, 0]

        return Deq
        
    def resistencia_zero(self, Rp, Rrs):
        """Calcula a resistência de sequência zero [mΩ/m].
        
            Parâmetros:
                Rp : número
                    Resistência positiva à corrente alternada [mΩ/m].
                    
                Rrs : número
                    Resistência de circuito de retorno pelo solo [mΩ/m]."""

        Rz = Rp + Rrs

        return Rz

    def reatancia_zero(self, resistividade):
        """Calcula a reatância de sequência zero [mΩ/m].
        
        INCOMPLETO"""


        Dc = 2 * self.raio_condutor()
        Rmg = 0.3895 * Dc
        Dca = self.diametro_externo()
        D = Dca  # teste
        Dmg = self.calcular_Dmg(D)
        Deq =  self.distancia_retorno_solo(resistividade)
        Xz = 0.2262 * np.log(Deq / (np.sqrt(Rmg + (Dmg**2), order = '3')))

        return Xz
    
    def impedancia_zero_solo(self): 
        """Calcula a impedância de sequência zero [mΩ/m].
        
        INCOMPLETO"""

        resistividade = 100 #teste
        Zp = self.impedancia_positiva_aterrada_um_ponto()
        Rp = np.real(Zp)
        Rrs = self.resistencia_circuito_retorno_solo(resistividade)
        Rz = self.resistencia_zero(Rp, Rrs)
        Xz = self.reatancia_zero(resistividade)
        Zz = np.complex(Rz, Xz)

        return Zz

    def impedancia_zero_blindagem(self): 

        resistividade = 100 #teste
        Zp = self.impedancia_positiva_aterrada_um_ponto()
        Rp = np.real(Zp)
        Rb = self.resistencia_blindagem()
        Rz = self.resistencia_zero(Rp, Rb)
        Xz = self.reatancia_zero(resistividade)
        Zz = np.complex(Rz, Xz)

        return Zz

    #def impedancia_zero_blindagem_solo(self):
        
     #   Zz = self.impedancia_zero_solo()
      #  Rz = np.real(Zz) 
=======
import pandas as pd
import numpy as np
from leituras import Leitura

leitura = Leitura() 
tab421 = leitura.tabela(sheet_name = "4.21")
tab421 = tab421.replace({'Cabo isolado em XLPE':'XLPE', 'Cabo isolado em EPR':'EPR'})
tab42 = leitura.tabela(sheet_name = "4.2")
tab46 = leitura.tabela(sheet_name = "4.6")
tab47 = leitura.tabela(sheet_name = "4.7")
tab48 = leitura.tabela(sheet_name = "4.8")
tab49 = leitura.tabela(sheet_name = "4.9")

class Condutor():
    """Parâmetros: 
            material_isolante : string
                Uma string que informa o tipo do material isolante: XLPE, EPR.

            tipo_condutor : string
                Uma string que informa o material do condutor: "Fio de alumínio duro"; 
                    "Fio de cobre duro"; "IACS – padrão internacional de cobre recozido"; 
                    "Zincado para alma de cabos de alumínio".

            fator_secao_tensao : string ou numero
                Um número para a seção do condutor, para a classe de tensão "8.7kV - 15kV";
                    para classes de tensão diferentes, inserir o número para a seção do condutor + ".1", ex: "300.1"."""
    def __init__(self, material_isolante, tipo_condutor, fator_secao_tensao, fator_diametro, tensao_linha):

        self.material_isolante = material_isolante
        self.tipo_condutor = tipo_condutor
        self.fator_secao_tensao = fator_secao_tensao
        self.fator_diametro = fator_diametro
        self.tensao_fase = tensao_linha / np.sqrt(3)

    def gradiente_potencial(self, e_is, e_imp, tensao_fase, B, Rc, A):
        """Calcula o gradiente de potencial a que fica submetido um vazio ou uma impureza qualquer no interior da isolação [kV/mm].
        
            Parâmetros:
                e_is : número
                    Constante dielétrica do material isolante.

                e_imp : número
                    Constante dielétrica do material que constitui a impureza.

                tensao_fase : número
                    Tensão de fase [kV].

                B : número
                    Distância entre o ponto considerado no interior da isolação e a superfície do condutor [mm].

                Rc : número
                    Raio do condutor [mm].

                A : número
                    Espessura da camada isolante [mm]."""

        # Variável que armazena o valor do gradiente de potencial
        Vb = (0.869 * (e_is / e_imp) * self.tensao_fase) / ((B + Rc) * np.log((Rc + A) / Rc))

        return Vb

    def raio_condutor(self):
        """Retorna o raio do condutor (Rc) [mm]."""
        
        # Variável que armazena o valor do raio do condutor após buscar na tabela
        Rc = (1/2) * tab421.loc[tab421['Tipo de isolação'] == self.material_isolante].loc[tab421['Caracteristica']
                                                                                    == 'Diâmetro do condutor - mm', [self.fator_secao_tensao]].values[0,0]
        return Rc

    def distancia_B(self):
        """Retorna a distância entre o ponto considerado no interior da isolação e a superfície do condutor (B) [mm]."""

        # Variável que armazena da distância B após buscar na tabela
        B = (1/2) * tab421.loc[tab421['Tipo de isolação'] == self.material_isolante].loc[tab421['Caracteristica']
                                                                                    == 'Espessura da isolação -mm', [self.fator_secao_tensao]].values[0,0]
        return B

    def espessura_camada_isolante(self):
        """Retorna a espessura da camada isolante (A) [mm]."""

        # Variável que armazena o valor da espessura da isolação após buscar na tabela
        A = tab421.loc[tab421['Tipo de isolação'] == self.material_isolante].loc[tab421['Caracteristica']
                                                                            == 'Espessura da isolação -mm', [self.fator_secao_tensao]].values[0,0]

        return A

    def funcao_constante_dieletrica_isolante(self):
        """Retorna a constante dieletrica do material isolante (e_is)."""

        # Variável que armazena o valor da constante dielétrica do material isolante após buscar na tabela
        constante_dieletrica_isolante = tab46.loc[tab46['Materiais Isolantes'] == self.material_isolante, [
            'ε']].values[0,0]

        return constante_dieletrica_isolante

    def funcao_constante_dieletrica_impureza(self, material_impureza):
        """Retorna a constante dielétrica do material que constitui a impureza (e_imp)."""

        # Variável que armazena o valor da constante dielétrica da impureza após buscar na tabela
        constante_dieletrica_impureza = tab46.loc[tab46['Materiais Isolantes'] == material_impureza, [
            'ε']].values[0,0]

        return constante_dieletrica_impureza

    def capacitancia_cabo(self, Dc, A, Ebi):
        """Calcula a capacitância do cabo [uF/km].
        
           Parâmetros:
                Dc : número
                    Diâmetro do condutor [mm].

                A : número
                    Espessura da camada isolante [mm].

                Ebi : número
                    Espessura da blindagem interna das firas semicondutores [mm]."""

        # Variável que armazena o valor do diâmetro sobre a isolação do material isolante
        Dsi = Dc + 2 * A + 2 * Ebi
        # Variável que recebe o valor da constante dielétrica do material
        constante_dieletrica_isolante = self.funcao_constante_dieletrica_isolante()
        # Variável que armazena o valor da capacitância calculada
        C = (0.0556 * constante_dieletrica_isolante) / (np.log(Dsi / (Dc + 2 * Ebi)))

        return C

    def perdas_dieletricas(self, C):
        """Calcula as perdas dielétricas do cabo [W/m].
        
            Parâmetros:
                C : número
                    Capacitância do cabo [uF/km]."""

        tangente_delta = tab46.loc[tab46['Materiais Isolantes']
                                == self.material_isolante, ['tg δ (20ºC)']].values[0,0]

        Pd = 0.3769 * C * (self.tensao_fase**2) * tangente_delta

        return Pd

    def perda_dieletrica_total(self, Pd, comprimento):
        """Calcula as perdas totais dielétricas do cabo [W].
        
            Parâmetros:
                Pd : número
                    Perdas dielétricas do cabo [W/m].
                    
                Comprimento: número
                    Comprimento do cabo [m]."""

        Pdt = Pd * comprimento

        return Pdt

    def diametro_externo(self):
        """Retorna o diâmetro externo do cabo [mm]."""

        Dca = tab421.loc[tab421['Tipo de isolação'] == self.material_isolante].loc[tab421['Caracteristica']
                                                                            == 'Diâmetro externo - mm', [self.fator_secao_tensao]].values[0,0]

        return Dca

    def fator_K(self, fator, encordoamento, fator_diametro):
        """Retorna o fator K.
        
            Parâmetros:
                INCOMPLETO"""

        if fator_diametro != 0:
            K = tab47.loc[tab47['Fator'] == fator].loc[tab47['Condutor'] == encordoamento, [fator_diametro]].values[0,0]
        else:
            K = tab47.loc[tab47['Fator'] == fator].loc[tab47['Condutor'] == encordoamento, ['Unnamed: 2']].values[0,0]

        return K

    def resistencia_cc(self, K1, K2, K3, p20, a20, Tc, S):
        """Calcula a resistência em corrente contínua a T°C [mΩ/m].
        
            Parâmetros:
                K1 : número
                    Fator que depende do diâmetro dos fios elementares do condutor e do tipo de encordoamento (Tabela 4.7).

                K2 : número
                    Fator que depende do tipo de encordoamento do condutor (Tabela 4.7).

                K3 : número
                    Fator que depende do tipo de reunião dos cabos componentes do cabo multipolar (Tabela 4.7).

                p20 : número
                    Resistividade do material condutor [Ωmm²/m].
                    
                a20 : número
                    Coeficiente de temperatura do material condutor [1/°C].
                    
                Tc : número
                    Temperatura do condutor [°C] (adotar normalmente a temperatura máxima admitida pela isolação).
                    
                S : número
                    Seção do condutor [mm²]."""

        Rcc = (1/S) * (1000 * K1 * K2 * K3 * p20) * (1 + a20 * (Tc - 20))

        return Rcc

    def componente_correcao_efeito_peculiar(self, Rcc):
        """Calcula a componente que corrige o efeito pelicular da distribuição de corrente na seção do condutor.
        
            Parâmetros:
                Rcc : número
                    Resistência em corrente contínua a T°C [mΩ/m]."""

        Fs = 0.15 / Rcc
        Ys = (Fs**2) / (192 + 0.8 * (Fs**2))

        return Ys

    def componente_correcao_proximidade_cabos(self, Ys, Dc, Dmg):
        """Calcula a componente que corrige o efeito de proximidade entre os cabos.

            Parâmetros:
                Ys : número
                    Componente que corrige o efeito pelicular da distribuição de corrente na seção do condutor.
                    
                Dc : número
                    Diâmetro do condutor [mm].
                    
                Dmg : número
                    Distância média geométrica do conjunto de cabos componentes [mm]."""

        Yp = Ys * ((Dc / Dmg)**2) * ((1.18 / (0.27 + Ys)) + 0.312 * ((Dc / Dmg)**2))

        return Yp

    def calcular_Dmg(self, D):
        """Calcula o diâmetro médio geométrico.

        INCOMPLETO"""

        return 1.26 * D

    def resistividade_condutor(self):
        """ --- Função que retorna a resistividade do condutor ----
        Primeiro argumento é o tipo do condutor"""

        resistividade = tab42.loc[tab42['Especificações'] ==
                                'Resistividade máxima a 20ºC (Ω/mm2/m)', [self.tipo_condutor]].values[0,0]

        return resistividade

    def coeficiente_temperatura(self):
        """ --- Função que retorna o coeficiente de temperatura do condutor ----
        Primeiro argumento é o tipo do condutor"""

        coeficiente_temperatura = tab42.loc[tab42['Especificações'] ==
                                            'Coeficiente de variação da resistência/ºC a 20ºC', [self.tipo_condutor]].values[0,0]
        return coeficiente_temperatura

    def reatancia_positiva(self, Dmg, Dc):
        """ ---- Função que calcula a reatância positiva ----
        Primeiro argumento é a distância média geométrica; Segundo argumento é o diâmetro do condutor"""

        Xp = 0.0754 * np.log((Dmg) / (0.779 * (Dc / 2)))

        return Xp

    def reatancia_blindagem(self):
        """ ---- Função que calcula a reatância da blindagem para um ponto de aterramento ----
        Primeiro argumento é a distância média geométrica; Segundo argumento é o diâmetro médio da blindagem"""

        Dca = self.diametro_externo()
        D = Dca  # teste
        Dmg = self.calcular_Dmg(D)
        Dc = 2 * self.raio_condutor()
        Ei = self.espessura_camada_isolante()
        Ebi = 1 #teste
        Ebe = 1 #teste
        Ebm = 1 #teste
        Dmb = self.diametro_medio_bindagem(Dc, Ei, Ebi, Ebe, Ebm)

        Xb = 0.0754 * np.log((2 * Dmg) / (Dmb))

        return Xb

    def acrescimo_componente_resistivo(self, Rb, Xb):
        # """ ---- Função que calcula o acréscimo ao componente resistivo da impedância de sequência positiva ----
        #     Primeiro argumento é a resistência da blindagem; Segundo argumento é a reatância da blindagem""""

        delta_Rb = Rb / (((Rb / Xb)**2) + 1)

        return delta_Rb

    def resistencia_blindagem(self):
        """ ---- Função que calcula a resistência da blindagem ----
            Primeiro argumento é o coeficiente de temperatura; Segundo argumento é a resistividade
            Terceiro argumento é a área da seção transversal; Quarto argumento é a temperatura da blindagem;
            Último argumento é a constante K4"""

        K4 = self.fator_K('K4', 'Fio ou encordoamento compacto', self.fator_diametro)
        resistividade = self.resistividade_condutor()
        coeficiente_temp = self.coeficiente_temperatura()
        Sb = 300#self.secao_blindagem(diametro_fio, intensidade_corrente)
        Tb = 90 #teste
        Rb = (1 + coeficiente_temp * (Tb - 20)) * (1000 * K4 * resistividade) / Sb

        return Rb

    def secao_blindagem(self, diametro_fio, intensidade_corrente):
        """ ---- Função que retorna a seção da blindagem ----
            Primeiro argumento é o diâmetro do fio; Segundo argumento é a intensidade da corrente que passa no fio"""

        Sb = tab48.loc[tab48['Diâmetro dos fios em mm'] == diametro_fio].loc[tab48['Intensidade máx. adm. em curto-circuito (1s) kA'] == intensidade_corrente, [
            'Seção da blindagem (mm²)']].values[0, 0]

        return Sb

    def reducao_indutancia(self, M, Rb, Xb):
        """ ---- Função que calcula a redução da indutância de sequência positiva ----
            Primeiro argumento é a resistência da blindagem; Segundo argumento é a reatância da blindagem à um ponto de aterramento"""

        delta_Lb = ((M) / (((Rb / Xb)**2) + 1))

        return delta_Lb

    def reducao_reatancia_positiva(self, Rb, Xb):
        """ ---- Função que calcula a redução da reatância de sequência positiva ----
            Primeiro argumento é a resistência da blindagem; Segundo argumento é a reatância da blindagem à um ponto de aterramento"""

        delta_Xb = ((Xb) / (((Rb / Xb)**2) + 1))

        return delta_Xb

    def acrescimos_resistencia_reatancia_positiva(self):

        Xb = self.reatancia_blindagem()
        Rb = self.resistencia_blindagem()

        delta_Rb = self.acrescimo_componente_resistivo(Rb, Xb)
        delta_Xb = self.reducao_reatancia_positiva(Rb, Xb)

        return delta_Rb, delta_Xb


    def diametro_medio_bindagem(self, Dc, Ei, Ebi, Ebe, Ebm):
        """ ---- Função que calcula o diâmetro médio da blindagem  ----
            Primeiro argumento é o diâmetro do condutor; Segundo argumento é a espessura da isolação;
            Terceiro argumento é a espessura da blindagem do interna; Quarto argumento é a espessura da blindagem externa;
            Último argumento é a espessura da blindagem metálica"""

        Dmb = Dc + 2 * Ei + 2 * Ebi + 2 * Ebe + (Ebm / 2)

        return Dmb

    def resistencia_positiva(self, Dmg, Dc):
        """ ---- Função que calcula a resistência positiva ----"""
        
        K1 = self.fator_K('K1', 'Fio ou encordoamento compacto', self.fator_diametro)
        K2 = self.fator_K('K2', 'Fio ou encordoamento compacto', 0)
        K3 = self.fator_K('K3', 'Cabos singelos', 0)
        p20 = self.resistividade_condutor()
        a20 = self.coeficiente_temperatura()
        Tc = 90  # teste
        S = 300
        Rcc = self.resistencia_cc(K1, K2, K3, p20, a20, Tc, S)
        Ys = self.componente_correcao_efeito_peculiar(Rcc)
        Yp = self.componente_correcao_proximidade_cabos(Ys, Dc, Dmg)
        Rp = Rcc * (1 + Ys + Yp)

        return Rp

    def reatancia_positiva_efetiva(self, Xp, delta_Xb):
        """ ---- Função que calcula a reatância positiva efetiva para varios pontos de aterramento ----
            Primeiro argumento é a reatância positiva para varios pontos de aterramento;
            último argumento é a redução da reatância positiva"""

        Xf = Xp - delta_Xb

        return Xf

    def resistencia_positiva_efetiva(self, Rp, delta_Rb):
        """ ---- Função que calcula a resistência positiva efetiva para varios pontos de aterramento ----
            Primeiro argumento é a resistência positiva para varios pontos de aterramento;
            último argumento é o acréscimo da resistência positiva"""

        Rf = Rp + delta_Rb

        return Rf

    def impedancia_positiva_aterrada_um_ponto(self):
        """ ---- Função que calcula a impedância positiva para apenas um ponto de aterramento, "(m Ohms) / m" ----

        Return:     Um float complexo"""

        Dc = 2 * self.raio_condutor()
        Dca = self.diametro_externo()
        D = Dca  # teste
        Dmg = self.calcular_Dmg(D)
        Rp = self.resistencia_positiva(Dmg, Dc)
        Xp = self. reatancia_positiva(Dmg, Dc)
        Zp = np.complex(Rp, Xp)

        return Zp

    def impedancia_positiva_aterrada_pontos(self):
        """ ---- Função que calcula a impedância positiva para vários pontos de aterramento ----
            Primeiro argumento é a resistência efetiva positiva; Segundo argumento é a reatância efetiva positiva"""

        Zp = self.impedancia_positiva_aterrada_um_ponto()
        Rp = np.real(Zp)
        Xp = np.imag(Zp)

        delta_Rb, delta_Xb = self.acrescimos_resistencia_reatancia_positiva()
        Rpf = self.resistencia_positiva_efetiva(Rp, delta_Rb)
        Xpf = self.reatancia_positiva_efetiva(Xp, delta_Xb)
        Zpf = np.complex(Rpf, Xpf)

        return Zpf

    def impedancia_negativa_aterrada_um_ponto(self):
        Zn =  self.impedancia_positiva_aterrada_um_ponto()
        
        return Zn

    def impedancia_negativa_aterrada_varios_ponto(self):
        Znf =  self.impedancia_positiva_aterrada_pontos()
        
        return Znf

    def resistencia_circuito_retorno_solo(self, resistividade):
        
        Rrs = tab49.loc[tab49['Resistividade do solo (Ω.m) '] == resistividade, ['Resistência do circuito de retorno pelo solo (mΩ/m)']].values[0, 0]
        return Rrs

    def distancia_retorno_solo(self, resistividade):

        Deq = tab49.loc[tab49['Resistividade do solo (Ω.m) '] == resistividade, ['Distância equivalente para o circuito de retorno (mm)']].values[0, 0]
        return Deq
        
    def resistencia_zero(self, Rp, resistividade, R):

        Rz = Rp + R

        return Rz

    def reatancia_zero(self, resistividade):

        Dc = 2 * self.raio_condutor()
        Rmg = 0.3895 * Dc
        Dca = self.diametro_externo()
        D = Dca  # teste
        Dmg = self.calcular_Dmg(D)
        Deq =  self.distancia_retorno_solo(resistividade)
        Xz = 0.2262 * np.log(Deq / (np.sqrt(Rmg + (Dmg**2), order = '3')))

        return Xz
    
    def impedancia_zero_solo(self): 

        resistividade = 100 #teste
        Zp = self.impedancia_positiva_aterrada_um_ponto()
        Rp = np.real(Zp)
        Rrs = self.resistencia_circuito_retorno_solo(resistividade)
        Rz = self.resistencia_zero(Rp, resistividade, Rrs)
        Xz = self.reatancia_zero(resistividade)
        Zz = np.complex(Rz, Xz)

        return Zz

    def impedancia_zero_blindagem(self): 

        resistividade = 100 #teste
        Zp = self.impedancia_positiva_aterrada_um_ponto()
        Rp = np.real(Zp)
        Rb = self.resistencia_blindagem()
        Rz = self.resistencia_zero(Rp, resistividade, Rb)
        Xz = self.reatancia_zero(resistividade)
        Zz = np.complex(Rz, Xz)

        return Zz

    #def impedancia_zero_blindagem_solo(self):
        
     #   Zz = self.impedancia_zero_solo()
      #  Rz = np.real(Zz) 
>>>>>>> origin/trabalhando_sabado
