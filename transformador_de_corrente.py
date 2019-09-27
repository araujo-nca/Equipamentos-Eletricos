import math 


class TransformadorDeCorrente(object):



    def __init__(self, potencia_nominal, tensao_nominal, tipo = None):
        self.potencia_nominal = potencia_nominal
        self.tensao_nominal = tensao_nominal

    # Corrente no secundário do Transformador de corrente
    @property
    def corrente_secundario(self):

        return 5

    # Carga nominal do transformador
    @property
    def carga_nominal(self):
        """Calcula a carga nominal que será ligada ao secundário do TC [Ω]."""

        return (self.potencia_nominal/self.corrente_secundario**2)

    # Carga ligada ao TC
    def carga_tc(self, soma_das_cargas_conectadas, comprimento_condutor, impedancia_condutor):
        """Calcula a carga efetiva do transformador de corrente [VA].
        
            Parâmetros:
                soma_das_cargas_conectadas: número
                    Soma das cargas correspondentes dos aparelhos de medição considerados [VA].

                comprimento_condutor: número
                    Comprimento do fio condutor do secundário [m].

                impedância_condutor: número
                    Impedância do condutor [Ω/m]."""

        # Variável que calcula e armazena o valor carga efetiva do TC
        carga_total = soma_das_cargas_conectadas + comprimento_condutor * impedancia_condutor * self.corrente_secundario**2

        return carga_total

    def fator_sobrecorrente(self, carga_secundario, carga_nominal, fator_sobrecorrente_nominal):
        """Calcula o fator de sobrecorrente quando a carga do TC é menor que a nominal [VA].
        
            Parâmetros:
                carga_secundario: número
                    Carga efetiva aplicada ao secundário do TC [VA].
                
                carga_nominal : número
                    Carga nominal do TC [VA].
                
                fator_sobrecorrente_nominal: número
                    Fator de sobrecorrente nominal (geralmente 20) [adimensional]."""        

        # variável que calcula e armazena o fator de sobrecorrente  
        sobrecorrente = fator_sobrecorrente_nominal* (carga_nominal/carga_secundario)

        return sobrecorrente
    
    def corrente_magnetizacao(self, forca_magnetizacao, k):
        """Calcula a corrente de magnetização de acordo com a saturação do núcleo [mA].
        
            Parâmetros:
                forca_magnetizacao: número
                    Força de magnetização [mA/m].
        
                k: número
                    Valor que depende do comprimento do caminho magnético e do número de espiras (Tabela 5.5)."""

        # Variável que calcula e armazena a corrente de magnetização
        magnetizacao = k * forca_magnetizacao

        return magnetizacao

    def tensao_secundario(self, corrente_secundario, resistencia_carga, resistencia_enrolamento, reatancia_carga, reatancia_enrolamento_secundario):
        """Calcula a tensão nos terminais secundários do TC em [V]

            Parâmetros:
                corrente_secundario: número
                    Corrente que circula no secundário [A].
                
                resistencia_carga: número
                    Resistência da carga [Ω].

                resistencia_enrolamento: número
                    Resistência do enrolamento secundário do TC [Ω].
                
                reatância_carga: número
                    Reatância da carga [Ω].

                reatancia_enrolamento_secundario: número
                    Reatância do enrolamento secundário do TC [Ω]."""

        # Calcula e armazena o valor de tensão nos terminais secundários
        tensao = corrente_secundario * math.sqrt((resistencia_carga + resistencia_enrolamento)**2 + (reatancia_carga + reatancia_enrolamento_secundario)**2)

        return tensao



