import numpy as np
from PIL import Image
 
class TP():
    """Parâmetros: 
            tensao_primaria_nominal : número
                Tensão nominal no primário do transformador [V].

            tensao_medida_secundario : número (opcional)
                Tensão medida no secundário do transformador [V]."""

    def __init__(self, tensao_primaria_nominal, tensao_medida_secundario = None):
        
        self.tensao_medida_secundario = tensao_medida_secundario
        self.tensao_primaria_nominal = tensao_primaria_nominal
        self.tensao_nominal_secundario = 115
        self.RTPn = None

        if self.tensao_medida_secundario:

            # Calcula o parâmetro RTP (Relação de transformaçãoo de potencial nominal)
            self.RTPn = self.tensao_primaria_nominal / self.tensao_nominal_secundario

            # Calcula a tensão primária não corrigida do transformador
            self.tensao_primario_nao_corrigida = self.RTPn * tensao_medida_secundario


    def RTPr(self, tensao_primaria_aplicada = None, RTPn = None, erro_fator_correcao_de_relacao = None, FCRp = None):
        """"""

        if tensao_primaria_aplicada and self.tensao_medida_secundario:
            # Calcula o parâmetro RTPr (Relação de transformação de potencial real)
            RTPr = tensao_primaria_aplicada / self.tensao_medida_secundario
        elif RTPn and erro_fator_correcao_de_relacao:
            RTPr = RTPn * (100 - erro_fator_correcao_de_relacao) / 100
        elif RTPn and FCRp:
            RTPr = RTPn * FCRp / 100
        else:
            print("Parametro nao identificado.")

        return RTPr

    def FCRr_e_FCRp(self, RTPr, RTPn = None):

        if self.RTPn:
            # Calcula o fator de correção de relação real
            FCRr = RTPr / self.RTPn
        elif RTPn:
            FCRr = RTPr / RTPn
        else:
            print("RTPn nao identificado.")

        # Calcula o fator de correção de relação percentual
        FCRp = FCRr * 100

        # Retorna duas saídas, FCP real e percentual
        return FCRr, FCRp

    def erro_fator_correcao_de_relacao(self, FCRp_ou_TensaoPrimarioAplicada):
        # Calcula o erro do fator de correção de relação (epsilon_p)

        if FCRp_ou_TensaoPrimarioAplicada > 200:
            # Entrada igual a tensão aplicada no primário
            TensaoPrimarioAplicada = FCRp_ou_TensaoPrimarioAplicada
            Ep = (self.RTPn * self.tensao_medida_secundario - TensaoPrimarioAplicada) * 100 / TensaoPrimarioAplicada
        else:
            # Entrada igual a FCRp
            FCRp = FCRp_ou_TensaoPrimarioAplicada
            Ep = 100 - FCRp

        return Ep

    def tensao_primario_real(self, Ep):

        # Variável que recebe a tensão no primário corrigida (valor real)
        v_primario_real = self.tensao_primario_nao_corrigida - (self.tensao_primario_nao_corrigida * Ep / 100)

        return v_primario_real

    def delta_tensao_primario(self, tensao_primario_aplicada, RTPn):

        v_primario_real = self.tensao_medida_secundario * RTPn
        delta_tensao_primario = tensao_primario_aplicada - v_primario_real

        return delta_tensao_primario

    def classe_de_exatidao(self, angulo_fase = None, FCRp = None):

        img_classe_exatidao = Image.open('figura_classedeexatidao.png')
        img_classe_exatidao.show()

        return
    
    def tensao_secundario(self, RTPn):
        
        v_secundario = self.tensao_primaria_nominal / RTPn

        return v_secundario
        
    def corrente_carga(self, potencia_carga, FP_carga, tensao_secundario):

        #Calcula a corrente na carga
        Ic = potencia_carga * FP_carga / tensao_secundario
        
        return Ic

    def queda_de_tensao_circuito(self, corrente_carga, resistencia_condutor, comprimento_condutor):

        #Variável que calcula a queda de tensão no circuito
        delta_v_circuito = corrente_carga * resistencia_condutor * (2 * comprimento_condutor) / 1000

        return  delta_v_circuito

    def fator_correcao_relacao_carga_total_secundaria(self, FCRp, tensao_secundario, FP_carga, corrente_carga, comprimento_condutor, resistencia_condutor, reatancia_condutor):

        Ic = corrente_carga
        Lc = comprimento_condutor
        Rc = resistencia_condutor
        Xc = reatancia_condutor
        FP = FP_carga
        theta_carga = np.arccos(FP)

        #Fator de correção de relação de carga secundária
        FCRct = FCRp / 100 + (Ic * 2 * Lc) / tensao_secundario * (Rc * FP + Xc * np.sin(theta_carga)) / 1000
        
        return FCRct

    def angulo_fase_total(self, angulo_fase, tensao_secundario, FP_carga, corrente_carga, comprimento_condutor, resistencia_condutor, reatancia_condutor):
        
        Ic = corrente_carga
        Lc = comprimento_condutor
        Rc = resistencia_condutor
        Xc = reatancia_condutor
        FP = FP_carga
        theta_carga = np.arccos(FP)

        #Calcula o desvio angular total
        gamma_ct = angulo_fase + (3.438 * Ic * 2 * Lc) / tensao_secundario * (Rc * np.sin(theta_carga) + Xc * FP) / 1000

        return gamma_ct