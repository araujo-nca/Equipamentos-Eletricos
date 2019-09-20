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
        
        return (self.potencia_nominal/self.corrente_secundario**2)

    # Carga ligada ao TC
    def carga_tc(self, soma_das_cargas_conectadas, comprimento_condutor, impedancia_condutor):
        
        carga_total = soma_das_cargas_conectadas + comprimento_condutor * impedancia_condutor * self.corrente_secundario**2

        return carga_total

    def fator_sobrecorrente(self, carga_secundario, carga_nominal, fator_sobrecorrente_nominal):

        sobrecorrente = fator_sobrecorrente_nominal* (carga_nominal/carga_secundario)

        return sobrecorrente
    
    def corrente_magnetizacao(self, forca_magnetizacao, k):

        magnetizacao = k * forca_magnetizacao

        return magnetizacao

    def tensao_secundario(self, corrente_secundario, resistencia_carga, resistencia_enrolamento, reatancia_carga, reatancia_enrolamento_secundario):

        tensao = corrente_secundario * math.sqrt((resistencia_carga + resistencia_enrolamento)**2 + (reatancia_carga + reatancia_enrolamento_secundario)**2)

        return tensao



