import numpy as np
from carga import Carga
 
class TP():

    def __init__(self, tensao_primario, fator_correcao, tensao_medida, grupo, contactores, potencia_carga):
        
        #Constroi o objeto de carga
        self.carga = Carga(contactores, potencia_carga) 
        #Recebe o parâmetro de tensão no primário
        self.tensao_primario = tensao_primario 
        # Recebe o parâmetro grupo do TP
        self.grupo = grupo
        #Recebe o parâmetro defator de correção
        self.fator_correcao = fator_correcao
        #Recebe o parâmetro de tensão de medida
        self.tensao_medida = tensao_medida
        #Calcula o parâmetro RTP (Relacao de transformacao de potencial)
        self.RTP = self.tensao_primario / 115
        #Calcula o parâmetro RTPr (Relacao de transformacao de potencial real)
        self.RTPr = self.tensao_primario / self.tensao_medida
        #Calcula o fator de correção de relação real
        self.FCRr = self.RTPr / self.RTP
        #Calcula o erro de relação
        self.ep = 100 - (self.FCRr * 100)

    def tensao_real_primario(self):

        #Variável que recebe a real tensão do primário
        V_real = (self.RTP * self.tensao_medida) - ((self.RTP * self.tensao_medida) * (self.ep) / 100)

        return V_real

    def classe_exatidao(self, erro_angulo_defasagem):

        #Variável que recebe a real tensão do primário
        V_real =  self.tensao_real_primario()
        #Váriavel que calcula a diferença de tensões 
        delta_tensao = self.tensao_primario - V_real
        
        return delta_tensao

    def tensao_secundaria(self):

        #Variável que calcula a tensão do secundário
        Vs = self.tensao_primario / self.RTP

        return Vs

    def corrente_carga(self, carga):

        #Variável que calcula a tensão do secundário
        Vs = self.tensao_secundaria()
        #Calcula a corrente na carga
        Ic = Vs / carga
        
        return Ic

    def queda_tensao_circuito(self, carga, comprimento_circuito):

        #Variável que calcula a correntre na carga
        Ic = self.corrente_carga(carga)
        #Variável que recebe a resistência do condutor
        Rc = 2.221 # retirar da tabela dos condutores
        #Variável que calcula a queda de tensão no circuito
        queda_vs = Ic * Rc * (2 * comprimento_circuito)

        return  queda_vs

    def fator_correcao_relacao_carga(self, carga, fator_potencia, comprimento_circuito):
        
        #Variável que recebe a resistência do condutor
        Rc = 2.2221 #teste
        #Variável que recebe a reatância do condutor
        Xc = 0.1207 #teste
        #Variável que calcula a correntre na carga
        Ic = self.corrente_carga(carga)
        #Variável que calcula a tensão do secundário
        Vs = self.tensao_secundaria()

        #Fator de correção de relação de carga secundária
        FCRct = self.FCRr + Ic * ((2 * comprimento_circuito) / Vs) * (Rc * fator_potencia  + Xc * np.sin(np.arccos(fator_potencia)))
        
        return FCRct


    def desvio_angular(self, carga, fator_potencia, comprimento_circuito):

        #Variável que recebe a resistência do condutor
        Rc = 2.2221 #teste
        #Variável que recebe a reatância do condutor
        Xc = 0.1207 #teste
        #Variável que calcula a correntre na carga
        Ic = self.corrente_carga(carga)
        #Variável que calcula a tensão do secundário
        Vs = self.tensao_secundaria()
        #calcula o desvio angular total
        gamma_ct = 10 + ((3.438 * Ic * (2 * comprimento_circuito)) / Vs) * (Rc * np.sin(np.arccos(fator_potencia)) + Xc * fator_potencia)

        return gamma_ct

    def determinar_transformador_potencial(self, contactores, potencia_carga):
        
        #Constrói o objeto carga
        self.carga = Carga(contactores, potencia_carga) #entrar parametros
        #Recebe os fatores de potência 
        Fp1, Fp2 = self.carga.fator_potencia()
        #Recebe as potências em regime permanente e regime curta duração 
        S_permanente, S_curta_duracao = self.carga.potencia_por_regime()
        #utilizara a tabela 6.5 para determinar o trafo potencial

    def constante_K_termica(self):

        if self.grupo == 1 or self.grupo == 2:
            
            return 1.33
        
        elif self.grupo == 3:
            
            return 3.6

    def potencia_termica(self):
        
        Zcn = self.carga.impedancia_carga()
        K = self.constante_K_termica()
        Vs = self.tensao_secundaria()
        Pth = 1.21 * K * (Vs ** 2) / (Zcn)

        return Pth