import numpy as np
from carga import Carga

 
class TP():

    def __init__(self, tensao_primario, fator_correcao, tensao_medida):
        
        self.tensao_primario = tensao_primario
        self.fator_correcao = fator_correcao
        self.tensao_medida = tensao_medida
        self.RTP = self.tensao_primario / 115
        self.RTPr = self.tensao_primario / self.tensao_medida
        self.FCRr = self.RTPr / self.RTP
        self.ep = 100 - (self.FCRr * 100)

    def tensao_real_primario(self):
    
        V_real = (self.RTP * self.tensao_medida) - ((self.RTP * self.tensao_medida) * (self.ep) / 100)

        return V_real

    def classe_exatidao(self, erro_angulo_defasagem):

        V_real =  self.tensao_real_primario()
        delta_tensao = self.tensao_primario - V_real
        
        return delta_tensao

    def tensao_secundaria(self):

        Vs = self.tensao_primario / self.RTP

        return Vs

    def corrente_carga(self, carga):

        Vs = self.tensao_secundaria()
        Ic = Vs / carga
        
        return Ic

    def queda_tensao_circuito(self, carga, comprimento_circuito):

        Ic = self.corrente_carga(carga)
        Rc = 2.221 # retirar da tabela dos condutores
        delta_vs = Ic * Rc * (2 * comprimento_circuito)

        return delta_vs

    def fator_correcao_relacao_carga(self, carga, fator_potencia, comprimento_circuito):
        
        Rc = 2.2221 #teste
        Xc = 0.1207 #teste
        Ic = self.corrente_carga(carga)
        Vs = self.tensao_secundaria()

        FCRct = self.FCRr + Ic * ((2 * comprimento_circuito) / Vs) * (Rc * fator_potencia  + Xc * np.sin(np.arccos(fator_potencia)))
        
        return FCRct

    
    def desvio_angular(self, carga, fator_potencia, comprimento_circuito):

        Rc = 2.2221 #teste
        Xc = 0.1207 #teste
        Ic = self.corrente_carga(carga)
        Vs = self.tensao_secundaria()
        gamma_ct = 10 + ((3.438 * Ic * (2 * comprimento_circuito)) / Vs) * (Rc * np.sin(np.arccos(fator_potencia)) + Xc * fator_potencia)

        return gamma_ct

    def determinar_transformador_potencia(self, contactores, potencia_carga):
        
        self.carga = Carga(contactores, potencia_carga) #entrar parametros
        Fp1, Fp2 = self.carga.fator_potencia()
        S_permanente, S_curta_duracao = self.carga.potencia_por_regime()
        #utilizara a tabela 6.5 para determinar o trafo potencial

    def constante_K_termica(self):

        #grupo = pegar da tabela 6.6
        #if grupo == 1 or grupo == 2:
         #   return 1.33
        #elif grupo == 3:
         #   return 3.6

    def potencia_termica(self):
        
        Zcn = self.carga.impedancia_carga()
        K = self.constante_K_termica():
        Vs = self.tensao_secundaria()
        Pth = 1.21 * K * (Vs ** 2) / (Zcn)

        return Pth