import pandas as pd
import numpy as np
from banco_dados import tab421, tab42, tab46, tab47, tab48, tab49
from dmg import Dmg

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
    
    def __init__(self, material_isolante, tipo_condutor, fator_secao_tensao):

        self.material_isolante = material_isolante
        self.tipo_condutor = tipo_condutor
        self.fator_secao_tensao = fator_secao_tensao
        self.dmg = Dmg()

    def gradiente_potencial(self, material_impureza, tensao_linha):
        """Calcula o gradiente de potencial a que fica submetido um vazio ou uma impureza qualquer no interior da isolação [kV/mm].
        
            Parâmetros:
                material_impureza : string
                    Material que constitui a impureza

                tensao_linha : número
                    Tensão de linha [kV]. 
                    
            Retorna :  Gradiente de potencial com bolha de impureza
                       Gradiente de potencial sem bolha de impureza 
                       Gradiente de potencial maximo 
                       Menor gradiente de potencial """
                        
            
        # recebe a constante dieletrica do isolante
        e_is = self.funcao_constante_dieletrica_isolante()
        # recebe a constante dieletrica da impureza
        e_imp = self.funcao_constante_dieletrica_impureza(material_impureza)
        # recebe a distancia B
        B = self.distancia_B()
        # recebe o raio do condutor
        Rc = self.raio_condutor()
        # recebe a espessura da camada isolante
        A = self.espessura_camada_isolante()
        # Variável que armazena o valor do gradiente de potencial com impureza
        Vb1 = (0.869 * (e_is / e_imp) * tensao_linha / np.sqrt(3)) / ((B + Rc) * np.log((Rc + A) / Rc))
        # Variável que armazena o valor do gradiente de potencial sem bolha de impureza
        Vb2 = (0.869 * tensao_linha / np.sqrt(3)) / ((B + Rc) * np.log((Rc + A) / Rc))
        # Variável que armazena o valor do gradiente de maximo
        Vmax = (0.869 * tensao_linha / np.sqrt(3)) / ((Rc) * np.log((Rc + A) / Rc))
        # Variável que armazena o menor gradiente de potencial 
        Vmin = (0.869 * tensao_linha / np.sqrt(3)) / ((A + Rc) * np.log((Rc + A) / Rc))
        # Variável que armazena o gradiente medio
        Vmedio = (1.37 * tensao_linha / np.sqrt(3)) / (Rc + A)

        return Vb1, Vb2, Vmax, Vmin, Vmedio

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

    def capacitancia_cabo(self, Ebi):
        """Calcula a capacitância do cabo [uF/km].
        
           Parâmetros:
                Ebi : número
                    Espessura da blindagem interna das fitas semicondutores [mm]."""

        # recebe o raio do condutor
        Dc = 2 * self.raio_condutor()
        # recebe a espessura da camada isolante
        A = self.espessura_camada_isolante()
        # Variável que armazena o valor do diâmetro sobre a isolação do material isolante
        Dsi = Dc + 2 * A + 2 * Ebi
        # Variável que recebe o valor da constante dielétrica do material
        constante_dieletrica_isolante = self.funcao_constante_dieletrica_isolante()
        # Variável que armazena o valor da capacitância calculada
        C = (0.0556 * constante_dieletrica_isolante) / (np.log(Dsi / (Dc + 2 * Ebi)))

        return C

    def perdas_dieletricas(self, Ebi, tensao_linha):
        """Calcula as perdas dielétricas do cabo [W/m]. 
            Parâmetros:
                Ebi : número
                    Espessura da blindagem interna das fitas semicondutores [mm]."""


        C = self.capacitancia_cabo(Ebi)

        tangente_delta = tab46.loc[tab46['Materiais Isolantes']
                                == self.material_isolante, ['tg δ (20ºC)']].values[0,0]

        Pd = 0.3769 * C * ((tensao_linha / np.sqrt(3))**2) * tangente_delta

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

    def diametro_externo(self, fator_secao_tensao):
        """Retorna o diâmetro externo do cabo [mm]."""

        Dca = tab421.loc[tab421['Tipo de isolação'] == self.material_isolante].loc[tab421['Caracteristica']
                                                                            == 'Diâmetro externo - mm', [fator_secao_tensao]].values[0,0]

        return Dca

    def calcular_fator_diametro(self):
        " Função que retorna o fator diametro para acessar a tabela 4.7"

        # Recebe o diametro do condutor
        Dc = 2 * self.raio_condutor()
        # Condição para o diametro do condutor
        if Dc == 0.1:
            fator_diametro = "0.1"
            return fator_diametro
        # Condição para o diametro do condutor
        elif 0.1 < Dc <= 0.31:
            fator_diametro = "0,1 - 0,31"
            return fator_diametro
        # Condição para o diametro do condutor
        elif 0.31 < Dc <= 0.91:
            fator_diametro =  "0,31 - 0,91"
            return fator_diametro
        # Condição para o diametro do condutor
        elif 0.91 < Dc <= 3.6:
            fator_diametro = "0,91 - 3,6"
            return fator_diametro
        # Condição para o diametro do condutor
        elif Dc > 3.6:
            fator_diametro = "> 3,6"
            return fator_diametro

    def fator_K(self, fator, encordoamento):
        """Retorna o fator K.
        
            Parâmetros:
                fator : string
                    Informa qual fator deve ser calculado : K1, K2, K3
                encordoamento: string
                    Informar qual tipo de encordoamento:
                        1. Fio ou encordoamento compacto
                        2. Encordoamento normal
                        3. Encordoamento normal (θ < 0,6 mm) 
                        4. Cabos singelos
                        5. Cabos multipolares """

        # Recebe o fator diametro para acessar a tabela 4.7
        fator_diametro = self.calcular_fator_diametro()
        # Condição para fator K1
        if fator == 'K1':
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

    def reatancia_positiva(self, Configuracao_cabos, Distancia=None, Distancia_1=None, Distancia_2=None, Distancia_3=None):
        """Calcula a reatância indutiva de sequência positiva [mΩ/m].
        
            Parâmetros:
                 configuracao_cabos : string
                    string que informa a topologia dos cabos:
                        1. Três_cabos_unipolares
                        2. Um_cabo_tripolar
                        3. Três_cabos_unipolares_em_triangulo_equilatero
                        4. Três_cabos_unipolares_igualmente_espacados
                        5. Três_cabos_unipolares_espacados_assimetricamente

                Distancia : numero
                    Numero que informa a distancia para o caso de tres_cabos_unipolares_em_triangulo_equilatero
                
                Distancia_1, Distancia_2, Distancia_ 3: numeros
                    Numeros que informam as distancia para os casos: 
                        Três_cabos_unipolares_igualmente_espacados
                        Três_cabos_unipolares_espacados_assimetricamente """

        # Variável que armazena o diametro do condutor
        Dc = 2 * self.raio_condutor()
        # Variável que recebe a distancia media geometrica
        Dmg = self.calcular_dmg(Configuracao_cabos, Distancia, Distancia_1, Distancia_2, Distancia_3)
        # Variável que recebe a reatancia positiva
        Xp = 0.0754 * np.log((Dmg) / (0.779 * (Dc / 2)))
       
        return Xp

    def reatancia_blindagem(self, Dmg, Ebi, Ebe, Ebm):
        """Calcula a reatância da blindagem para um ponto de aterramento [mΩ/m].

            Parâmetros:
                Dmg :  Distância média geométrica [mm]
                Ebi :  Espessura da blindagem interna [mm]
                Ebe :  Espesura da blindagem externa [mm]
                Ebm :  Espessura da blindagem metálica [mm]

            Retorna um float para reatância da blindagem [mm] """

        # Variável que armazena o diâmetro do condutor
        Dc = 2 * self.raio_condutor()
        # Variável que armazena a espessura da camada isolante
        Ei = self.espessura_camada_isolante()
        # Variável que armazena o diâmetro médio da blindagem
        Dmb = self.diametro_medio_blindagem(Dc, Ei, Ebi, Ebe, Ebm)
        # Variável que armazena o valor da reatância da blindagem
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

    def resistencia_blindagem(self, Tb, K4):
        """Calcula a resistência da blindagem [mΩ/m]."""

        resistividade = self.resistividade_condutor()
        coeficiente_temp = self.coeficiente_temperatura()
        Sb = 6.5#self.secao_blindagem(diametro_fio, intensidade_corrente)
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

    def acrescimos_resistencia_reatancia_positiva(self, Tb, Dmg, K4, Ebi, Ebe, Ebm):
        """Retorna os valores de acréscimo das componentes resistiva e indutiva (delta_Rb, delta_Xb) [mΩ/m, Ω/km]."""

        Xb = self.reatancia_blindagem(Dmg, Ebi, Ebe, Ebm)
        Rb = self.resistencia_blindagem(Tb, K4)
        
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
    
    def calcular_dmg(self, Configuracao_cabos, Distancia, Distancia_1, Distancia_2, Distancia_3):
        """ Função que calcula a distancia media geometrica """

        # Variavel que armazena o diametro do condutor
        Dc = 2 * self.raio_condutor()
        # condicao para calcular a distancia media geometrica
        if Configuracao_cabos == "Três_cabos_unipolares":
            Dmg = self.dmg.tres_cabos_unipolares(Dc)
            return Dmg
        # condicao para calcular a distancia media geometrica
        elif Configuracao_cabos == "Um_cabo_tripolar":
            Dmg = self.dmg.um_cabo_tripolar(Dc)
            return Dmg
        # condicao para calcular a distancia media geometrica
        elif Configuracao_cabos == "Três_cabos_unipolares_em_triangulo_equilatero":
            Dmg = self.dmg.tres_cabos_unipolares_em_triangulo_equilatero(Distancia)
            return Dmg
        # condicao para calcular a distancia media geometrica
        elif Configuracao_cabos == "Três_cabos_unipolares_igualmente_espacados":
            Dmg = self.dmg.tres_cabos_unipolares_igualmente_espacados(Distancia)
            return Dmg
        # condicao para calcular a distancia media geometrica
        elif Configuracao_cabos == "Três_cabos_unipolares_espacados_assimetricamente":
            Dmg = self.dmg.tres_cabos_unipolares_espacados_assimetricamente(Distancia_1, Distancia_2, Distancia_3)
            return Dmg

        
    def resistencia_positiva(self, Tc, Configuracao_cabos, Distancia=None, Distancia_1=None, Distancia_2=None, Distancia_3=None):
        """Calcula a resistência positiva à corrente alternada [mΩ/m].
        
            Parâmetros:
                Tc : número
                    Temperatura do condutor [°C]

                configuracao_cabos : string
                    string que informa a topologia dos cabos:
                        1. Três_cabos_unipolares
                        2. Um_cabo_tripolar
                        3. Três_cabos_unipolares_em_triangulo_equilatero
                        4. Três_cabos_unipolares_igualmente_espacados
                        5. Três_cabos_unipolares_espacados_assimetricamente

                Distancia : numero
                    Numero que informa a distancia para o caso de tres_cabos_unipolares_em_triangulo_equilatero
                
                Distancia_1, Distancia_2, Distancia_ 3: numeros
                    Numeros que informam as distancia para os casos: 
                        Três_cabos_unipolares_igualmente_espacados
                        Três_cabos_unipolares_espacados_assimetricamente
                    """
        # Variavel que armazena o diametro do condutor
        Dc = 2 * self.raio_condutor()
        # Variavel que armazenaa constante K1
        K1 = self.fator_K('K1', 'Fio ou encordoamento compacto')
        # Variavel que armazenaa constante K2
        K2 = self.fator_K('K2', 'Fio ou encordoamento compacto')
        # Variavel que armazenaa constante K3
        K3 = self.fator_K('K3', 'Cabos singelos')
        # Variavel que armazena a resistividade do condutor
        p20 = self.resistividade_condutor()
        # Variavel que armazena o coeficiente de temperatura
        a20 = self.coeficiente_temperatura()
        # Variavel que armazena a secao do condutor
        S = 300
        # Variável que recebe a resistencia em corrente continua
        Rcc = self.resistencia_cc(K1, K2, K3, p20, a20, Tc, S)
        # Variável que recebe a componente de correção do efeito peculiar
        Ys = self.componente_correcao_efeito_peculiar(Rcc)
        # Variável que recebe a distancia media geometrica
        Dmg = self.calcular_dmg(Configuracao_cabos, Distancia, Distancia_1, Distancia_2, Distancia_3)
        # Variável que recebe a componente de correção de proximidades dos cabos
        Yp = self.componente_correcao_proximidade_cabos(Ys, Dc, Dmg)
        # Variável que recebe a resistência positiva
        Rp = Rcc * (1 + Ys + Yp)

        return Rp

    def reatancia_positiva_efetiva(self, Xp, delta_Xb):
        """Calcula a reatância positiva efetiva para vários pontos de aterramento [mΩ/m].
        
            Parâmetros:
                Xp : número
                    Reatância indutiva de sequência positiva [mΩ/m].
                    
                delta_Xb : número
                    Componente de redução da reatância de sequência positiva [Ω/km]."""

        # Variável que recebe a reatância efetiva
        Xf = Xp - delta_Xb/10e3

        return Xf

    def resistencia_positiva_efetiva(self, Rp, delta_Rb):
        """Calcula a resistência positiva efetiva para vários pontos de aterramento [mΩ/m].
        
            Parâmetros:
                Rp : número
                    Resistência positiva à corrente alternada [mΩ/m].
                    
                delta_Rb : número
                    Componente de acréscimo resistivo da impedância de sequência positiva [mΩ/m]."""

        # Variável que recebe a resistência efetiva
        Rf = Rp + delta_Rb

        return Rf

    def impedancia_positiva_aterrada_um_ponto(self, Tc, Configuracao_cabos, Distancia=None, Distancia_1=None, Distancia_2=None, Distancia_3=None):
        """Calcula a impedância de sequência positiva para apenas um ponto de aterramento [mΩ/m].
            
            Parâmetros:
                Tc : número
                    Temperatura do condutor [°C]

                configuracao_cabos : string
                    string que informa a topologia dos cabos:
                        1. Três_cabos_unipolares
                        2. Um_cabo_tripolar
                        3. Três_cabos_unipolares_em_triangulo_equilatero
                        4. Três_cabos_unipolares_igualmente_espacados
                        5. Três_cabos_unipolares_espacados_assimetricamente

                Distancia : numero
                    Numero que informa a distancia para o caso de tres_cabos_unipolares_em_triangulo_equilatero
                
                Distancia_1, Distancia_2, Distancia_ 3: numeros
                    Numeros que informam as distancia para os casos: 
                        Três_cabos_unipolares_igualmente_espacados
                        Três_cabos_unipolares_espacados_assimetricamente"""
        
        # Variável que armazena a resistência positiva
        Rp = self.resistencia_positiva(Tc, Configuracao_cabos, Distancia, Distancia_1, Distancia_2, Distancia_3)
        # Variável que armazena a reatância positiva
        Xp = self. reatancia_positiva(Configuracao_cabos, Distancia, Distancia_1, Distancia_2, Distancia_3)
        # Variável que armazena a impedância positiva aterrada em um ponto
        Zp = np.complex(Rp, Xp)

        return Zp

    def impedancia_positiva_aterrada_pontos(self, Tc, Tb, K4, Ebi, Ebe, Ebm, Corrente_condutor, comprimento_linha, Configuracao_cabos, Distancia=None, Distancia_1=None, Distancia_2=None, Distancia_3=None):
        """Calcula a impedância de sequência positiva para vários pontos de aterramento [mΩ/m]
            Calcula a tensão entre a blindagem e a terra [mV/m]
            Calcula a corrent circulante dentro da blindagem [A]
            Calcula as perdas na linha por efeito joule [W].

             Parâmetros:
                Tc : número
                    Temperatura do condutor [°C]

                Tb : número
                    Temperatura máxima que a blindagem suporta [°C]

                K4 : Fator que leva em consideração o tipo de blindagem

                Ei : número
                    Espessura da isolação [mm].
                    
                Ebi : número
                    Espessura da blindagem interna das fitas semicondutores, não condutora [mm].
                    
                Ebe : número
                    Espessura da blindagem externa de campo elétrico, não condutora [mm].
                    
                Ebm : número
                    Espessura da blindagem metálica [mm]

                Corrente_condutor :  número
                    Corrente que passa no condutor [A]

                Comprimento da linha: número
                    Comprimento da linha [M]

                configuracao_cabos : string
                    string que informa a topologia dos cabos:
                        1. Três_cabos_unipolares
                        2. Um_cabo_tripolar
                        3. Três_cabos_unipolares_em_triangulo_equilatero
                        4. Três_cabos_unipolares_igualmente_espacados
                        5. Três_cabos_unipolares_espacados_assimetricamente

                Distancia : numero
                    Numero que informa a distancia para o caso de tres_cabos_unipolares_em_triangulo_equilatero
                
                Distancia_1, Distancia_2, Distancia_ 3: numeros
                    Numeros que informam as distancia para os casos: 
                        Três_cabos_unipolares_igualmente_espacados
                        Três_cabos_unipolares_espacados_assimetricamente
                        
                Retorna a impedância positiva para o condutor aterrado em vários pontos, 
                    tensão entre a blindagem e a terra, corrente que circula na blindagem,
                    perdas na linha por efeito joule"""

        # Variável que armazena a impedância positiva aterrada apenas em um ponto             
        Zp = self.impedancia_positiva_aterrada_um_ponto(Tc, Configuracao_cabos, Distancia, Distancia_1, Distancia_2, Distancia_3)
        # Recebe a resistência positiva
        Rp = np.real(Zp)
        # Recebe a reatância positiva
        Xp = np.imag(Zp)
        # Variável que armazena o diâmetro do condutor
        Dc = 2 * self.raio_condutor()
        # Variável que armazena a espessura isolante
        Ei = self.espessura_camada_isolante()
        # Variável que recebe a distancia media geometrica
        Dmg = self.calcular_dmg(Configuracao_cabos, Distancia, Distancia_1, Distancia_2, Distancia_3)
        # Variáveis que recebem as correções para a resistência positiva e reatância positiva
        delta_Rb, delta_Xb = self.acrescimos_resistencia_reatancia_positiva(Tb, Dmg, K4, Ebi, Ebe, Ebm)
        # Variável que armazena a resitência positiva efetiva
        Rpf = self.resistencia_positiva_efetiva(Rp, delta_Rb)
        # Variável que armazena a reatância positiva efetiva
        Xpf = self.reatancia_positiva_efetiva(Xp, delta_Xb)
        # Variável que armazena a impedância positiva aterrada em vários pontos
        Zpf = np.complex(Rpf, Xpf)
        # Variável que armazena diâmetro média da blindagem
        Dmb = self.diametro_medio_blindagem(Dc, Ei, Ebi, Ebe, Ebm)
        # Variável que armazena a tensão entre a blindagem e a terra
        Vbt = 0.0754 * Corrente_condutor * np.log((2 * Dmg) / Dmb)
        # Variável que armazena a resistência da blindagem
        Rb = self.resistencia_blindagem(Tb, K4)
        # Variável que armazena a reatância da blindagem
        Xb = self.reatancia_blindagem(Dmg, Ebi, Ebe, Ebm)
        # Variável que calcula a corrente circulante na blindagem
        Icb = Vbt / np.sqrt(((Rb ** 2) + (Xb ** 2)))
        # Variável que armazena as perdas nas linhas por efeito joule
        Pl = 1e-3 * Rb * (Icb ** 2) * comprimento_linha

        return Zpf, Vbt, Icb, Pl
    
    def impedancia_negativa_aterrada_um_ponto(self, Tc, Configuracao_cabos, Distancia=None, Distancia_1=None, Distancia_2=None, Distancia_3=None):
        """Calcula a impedância de sequência negativa para apenas um ponto de aterramento [mΩ/m]."""

        Zn =  self.impedancia_positiva_aterrada_um_ponto(Tc, Configuracao_cabos, Distancia, Distancia_1, Distancia_2, Distancia_3)
        
        return Zn

    def impedancia_negativa_aterrada_varios_pontos(self, Tc, Tb, K4, Ebi, Ebe, Ebm, Corrente_condutor, comprimento_linha, Configuracao_cabos, Distancia=None, Distancia_1=None, Distancia_2=None, Distancia_3=None):
        """Calcula a impedância de sequência negativa para vários pontos de aterramento [mΩ/m]."""

        Znf =  self.impedancia_positiva_aterrada_pontos(Tc, Tb, K4, Ebi, Ebe, Ebm, Corrente_condutor, comprimento_linha, Configuracao_cabos, Distancia, Distancia_1, Distancia_2, Distancia_3)
        
        return Znf

    def resistencia_circuito_retorno_solo(self, resistividade):
        """Retorna a resistência de circuito de retorno pelo solo [mΩ/m].
        
            Parâmetros:
                resistividade : número
                    Resistividade do solo [Ω/m]."""
        
        Rrs = tab49.loc[tab49['Resistividade do solo (Ω.m)'] == resistividade, ['Resistência do circuito de retorno pelo solo (mΩ/m)']].values[0, 0]

        return Rrs

    def distancia_retorno_solo(self, resistividade):
        """Retorna a distância equivalente para o circuito de retorno [mm].
        
            Parâmetros:
                resistividade : número
                    Resistividade do solo [Ω/m]."""

        Deq = tab49.loc[tab49['Resistividade do solo (Ω.m)'] == resistividade, ['Distância equivalente para o circuito de retorno (mm)']].values[0, 0]

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

    def reatancia_zero(self, resistividade, Configuracao_cabos, Distancia, Distancia_1, Distancia_2, Distancia_3):
        """Calcula a reatância de sequência zero [mΩ/m].
        
        INCOMPLETO"""

        Dc = 2 * self.raio_condutor()
        Deq =  self.distancia_retorno_solo(resistividade)
        # Variável que recebe a distancia media geometrica
        Dmg = self.calcular_dmg(Configuracao_cabos, Distancia, Distancia_1, Distancia_2, Distancia_3)
        Xz = 0.2262 * np.log(Deq / (((0.3895 * Dc) * (Dmg**2)) ** (1/3)))
        
        return Xz
    
    def impedancia_zero_solo(self,  resistividade, Tc, Configuracao_cabos, Distancia=None, Distancia_1=None, Distancia_2=None, Distancia_3=None): 
        """Calcula a impedância de sequência zero [mΩ/m].
        
        INCOMPLETO"""

        Zp = self.impedancia_positiva_aterrada_um_ponto( Tc, Configuracao_cabos, Distancia, Distancia_1, Distancia_2, Distancia_3)
        Rp = np.real(Zp)
        Rrs = self.resistencia_circuito_retorno_solo(resistividade)
        Rz = self.resistencia_zero(Rp, Rrs)
        Xz = self.reatancia_zero(resistividade, Configuracao_cabos, Distancia, Distancia_1, Distancia_2, Distancia_3)
        Zz = np.complex(Rz, Xz)

        return Zz

    def impedancia_zero_blindagem_aterrada_um_ponto(self, resistividade, Tc, Tb, K4, Configuracao_cabos, Ebi, Ebe, Ebm, Distancia=None, Distancia_1=None, Distancia_2=None, Distancia_3=None): 

    
        Zp = self.impedancia_positiva_aterrada_um_ponto( Tc, Configuracao_cabos, Distancia, Distancia_1, Distancia_2, Distancia_3)
        Rp = np.real(Zp)
        Rb = self.resistencia_blindagem(Tb, K4)
        Rz = self.resistencia_zero(Rp, Rb)
        Ei = self.espessura_camada_isolante()
        Dc = 2 * self.raio_condutor()
        # Variável que armazena diâmetro média da blindagem
        Dmb = self.diametro_medio_blindagem(Dc, Ei, Ebi, Ebe, Ebm)
        # Variável que armazena o raio médio geométrico
        Rmg = (0.3895 * Dc)
        # Variável que armazena a reatância senquencia zero
        Xz = 0.2262 * np.log((Dmb / (2 * Rmg)) ** (1/3)) 
 
        Zz = np.complex(Rz, Xz)

        return Zz

    def impedancia_zero_blindagem_solo(self, Rb, Rrs, Deq, Dmb, Dmg):
        
        Rcb = Rb + Rrs
        Xcb = 0.2262 * np.log(Deq / (((Dmb * (Dmg ** 2)) / 2) ** (1/3)))
        Zcb = np.complex(Rcb, Xcb)

        return Zcb

    def impedancia_relativa_condutor(self, Rb, Rrs, Deq, Rmg, Dmg):

        Rco = Rb + Rrs
        Xco = 0.2262 * np.log(Deq / (((Rmg * (Dmg ** 2)) / 2) ** (1/3)))
        
        Zco = np.complex(Rco, Xco)
    
        return Zco

    def impedancia_efeito_mutuo_cabos(self, Rrs, Deq, Dmb, Dmg):

        Rm = Rrs
        Xm = 0.2262 * np.log(Deq / (((Dmb * (Dmg ** 2)) / 2) ** (1/3)))

        Zm = np.complex(Rm, Xm)

        return Zm

    def impedancia_sequencia_zero(self, resistividade, Tb, K4, Ebi, Ebe, Ebm, Configuracao_cabos, Distancia=None, Distancia_1=None, Distancia_2=None, Distancia_3=None):

        Dc = 2 * self.raio_condutor()
        Rb = self.resistencia_blindagem(Tb, K4)
        Rrs = self.resistencia_circuito_retorno_solo(resistividade)
        Deq = self.distancia_retorno_solo(resistividade)
        Ei = self.espessura_camada_isolante()
        Dmb = self.diametro_medio_blindagem(Dc, Ei, Ebi, Ebe, Ebm)
        Dmg = self.calcular_dmg(Configuracao_cabos, Distancia, Distancia_1, Distancia_2, Distancia_3)
        # Variável que armazena o raio médio geométrico
        Rmg = (0.3895 * Dc)

        Zcb = self.impedancia_zero_blindagem_solo(Rb, Rrs, Deq, Dmb, Dmg)
        Zco = self.impedancia_relativa_condutor(Rb, Rrs, Deq, Rmg, Dmg)
        Zm = self. impedancia_efeito_mutuo_cabos(Rrs, Deq, Dmb, Dmg)

        Z0 = Zco - (Zm ** 2) / Zcb

        return Z0